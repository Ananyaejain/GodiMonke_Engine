import unittest
import sys
import shutil
import json
from pathlib import Path
from unittest.mock import patch
from .runner import run_benchmark, BudgetExceeded, TokenLimitExceeded, BudgetAccountingError, generate_individual_run_id, build_request
from .scorer import score_verification, score_copy, validate_schema, extract_numbers
from .provider import FakeProvider
from .config import load_fixtures, load_schemas

class TestBenchmarkHarness(unittest.TestCase):
    def setUp(self):
        self.fixtures = load_fixtures()
        self.f_01 = self.fixtures["F01_UNION_BUDGET_CAPEX"]
        self.valid_caveats = self.f_01["gold"]["material_caveats"]

    def test_01_five_fixtures(self):
        self.assertEqual(len(self.fixtures), 5)
        self.assertEqual(len(set(self.fixtures.keys())), 5)

    def test_02_schemas_parse(self):
        v, c = load_schemas()
        self.assertIn("type", v)
        self.assertIn("type", c)

    def test_03_arbitrary_number_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "value 8888.88", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_04_changed_number_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "value 13.22", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_05_numeric_formatting_accepted(self):
        # 3.2 and 3.20 treated equivalent
        self.assertEqual(extract_numbers("3.2"), extract_numbers("3.20"))
        # 146195 / 146,195 / 1,46,195 equivalent
        self.assertEqual(extract_numbers("146195"), extract_numbers("146,195"))
        self.assertEqual(extract_numbers("1,46,195"), extract_numbers("146,195"))

    def test_06_invented_date_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "happened in 2099-01-01", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_07_invented_quote_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "They said 'This is fake'", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_08_unsupported_claim_id(self):
        output = {"format": "GM-SINGLE-01", "slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["FAKE-CLAIM"]}]}]}
        res = score_copy(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_09_unsupported_source_id(self):
        output = {"verdict": "SUPPORTED", "evidence_assessment": [{"source_id": "FAKE-SRC", "assessment": "SUPPORTS"}], "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_10_missing_caveat_not_critical(self):
        output = {"verdict": "SUPPORTED", "material_caveats": [], "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}]}
        res = score_verification(output, self.f_01, True)
        self.assertFalse(res["critical_fail"])
        self.assertEqual(res["caveat_retention"], 0)

    def test_11_unrelated_caveat_not_critical(self):
        output = {"verdict": "SUPPORTED", "material_caveats": ["This is a fake caveat"], "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}]}
        res = score_verification(output, self.f_01, True)
        self.assertFalse(res["critical_fail"])
        self.assertEqual(res["caveat_retention"], 0)

    def test_12_uncertainty_promoted_is_critical(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "This is 100% certain and a confirmed fact.", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_13_wrong_role_loses_points(self):
        # SRC-F01-A should be SUPPORTS
        output = {"verdict": "SUPPORTED", "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "CONTRADICTS"}], "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertEqual(res["evidence_integrity"], 0)
        self.assertEqual(res["semantic_evidence_fidelity"], "NEEDS_HUMAN_SCORE")

    def test_14_semantic_scores_remain_human(self):
        output = {"format": "GM-SINGLE-01", "slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["CLM-F01-1"]}]}]}
        res = score_copy(output, self.f_01, True)
        self.assertEqual(res["semantic_factual_fidelity"], "NEEDS_HUMAN_SCORE")
        self.assertEqual(res["final_score"], "NEEDS_HUMAN_SCORE")

    def test_15_wrong_format_loses_template_points(self):
        # Format requested: GM-SINGLE-01, we provide GM-CAROUSEL-01
        output = {"format": "GM-CAROUSEL-01", "slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["CLM-F01-1"]}]}]}
        res = score_copy(output, self.f_01, True)
        self.assertEqual(res["concision_template_fit"], 0)

    def test_16_carousel_slide_counts(self):
        f_car = dict(self.f_01)
        f_car["copy_format"] = "GM-CAROUSEL-01"
        # 1 slide -> 0 pts
        out1 = {"format": "GM-CAROUSEL-01", "slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["CLM-F01-1"]}]}]}
        res1 = score_copy(out1, f_car, True)
        self.assertEqual(res1["concision_template_fit"], 0)
        # 3 slides -> 10 pts
        out3 = {"format": "GM-CAROUSEL-01", "slides": [out1["slides"][0]] * 3}
        res3 = score_copy(out3, f_car, True)
        self.assertEqual(res3["concision_template_fit"], 10)

    def test_17_post_call_accounting_discrepancy(self):
        import benchmarks.model_selection.harness.runner as run_module
        req = {"track": "verification", "max_input_tokens": 1000, "max_output_tokens": 100, "route_config": {"provider": "dummy", "model": "dummy"}}
        with self.assertRaises(BudgetAccountingError):
            # est_cost=0.1, actual_cost=15.0
            run_module.process_call(FakeProvider("ACTUAL_COST_FAIL"), req, "F01", 1, 100.0, 0.0, {"per_call_hard_cap_inr": 20.0}, {}, Path("tmp"))

    def test_18_actual_per_call_cap(self):
        import benchmarks.model_selection.harness.runner as run_module
        req = {"track": "verification", "max_input_tokens": 1000, "max_output_tokens": 100, "route_config": {"provider": "dummy", "model": "dummy"}}
        with self.assertRaises(BudgetAccountingError):
            run_module.process_call(FakeProvider("ACTUAL_COST_FAIL"), req, "F01", 1, 100.0, 0.0, {"per_call_hard_cap_inr": 10.0}, {}, Path("tmp"))

    def test_19_perfect_run_invariants(self):
        session, calls = run_benchmark("PERFECT")
        self.assertEqual(len(calls), 90)
        valid_calls = sum(1 for c in calls if c["valid"])
        self.assertEqual(valid_calls, 90)
        cf_calls = sum(1 for c in calls if c["critical_fail"])
        self.assertEqual(cf_calls, 0)
        shutil.rmtree(Path(f"benchmarks/model_selection/results/{session}"))

    @patch("socket.socket")
    def test_20_network_blocked(self, mock_socket):
        mock_socket.side_effect = Exception("Network blocked")
        session, calls = run_benchmark("PERFECT")
        self.assertEqual(len(calls), 90)
        shutil.rmtree(Path(f"benchmarks/model_selection/results/{session}"))

    def test_21_doctor_jsonschema(self):
        import benchmarks.model_selection.harness.__main__ as main_module
        with patch('sys.exit') as mock_exit:
            main_module.doctor()
            mock_exit.assert_not_called()

    def test_22_gold_leakage_isolation(self):
        from .scorer import get_allowed_facts, get_sanitized_for_extractor
        f_leak = dict(self.f_01)
        f_leak["gold"] = dict(f_leak["gold"])
        f_leak["gold"]["material_caveats"] = ["This caveat contains hidden number 7777.77"]

        sanitized = get_sanitized_for_extractor(f_leak)
        allowed_nums, _, _, _, _ = get_allowed_facts(sanitized)
        self.assertNotIn(7777.77, allowed_nums)

        output = {"verdict": "SUPPORTED", "rationale_summary": "I am leaking 7777.77", "material_caveats": []}
        res = score_verification(output, f_leak, True)
        self.assertTrue(res["critical_fail"])

    def test_23_provider_boundary_isolation(self):
        from .config import sanitize_fixture, verify_no_leakage
        from .runner import build_request
        import json

        f_sentinel = dict(self.f_01)
        f_sentinel["gold"] = dict(f_sentinel["gold"])
        f_sentinel["gold"]["material_caveats"] = ["GOLD_SECRET_7XQ9", "7777.77"]

        sanitized = sanitize_fixture(f_sentinel)
        verify_no_leakage(sanitized)

        req = build_request("verification", "prompt", sanitized, {}, {"provider": "dummy", "model": "dummy"}, {"verification": {"max_output_tokens": 100, "max_input_tokens": 100, "max_output_tokens_by_route": {}}})

        def assert_no_sentinel(obj):
            s = json.dumps(obj)
            self.assertNotIn("GOLD_SECRET_7XQ9", s)
            self.assertNotIn("7777.77", s)

        assert_no_sentinel(req)

        provider = FakeProvider("PERFECT")
        # FakeProvider inputs
        assert_no_sentinel(req)

        res = provider.run_verification(req, {})
        # FakeProvider output
        assert_no_sentinel(res)

        # simulated artifacts
        raw_artifact = res
        normalized_artifact = {"run_id": "test", "output": res["output"]}
        assert_no_sentinel(raw_artifact)
        assert_no_sentinel(normalized_artifact)
