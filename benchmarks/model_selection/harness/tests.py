import unittest
import sys
import shutil
import json
from pathlib import Path
from unittest.mock import patch
from .runner import run_benchmark, BudgetExceeded, TokenLimitExceeded, generate_individual_run_id, build_request
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

    def test_05_arbitrary_number_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "value 8888.88", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_06_changed_number_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "value 13.22", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_07_numeric_formatting_accepted(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "value 12.22", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertFalse(res["critical_fail"])
        self.assertIn("146195", extract_numbers("1,46,195"))

    def test_08_invented_date_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "happened in 2099-01-01", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_09_invented_quote_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "They said 'This is fake'", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_10_unsupported_claim_id(self):
        output = {"slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["FAKE-CLAIM"]}]}]}
        res = score_copy(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_11_unsupported_source_id(self):
        output = {"verdict": "SUPPORTED", "evidence_assessment": [{"source_id": "FAKE-SRC", "assessment": "SUPPORTS"}], "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_12_correct_caveat_retained(self):
        output = {"verdict": "SUPPORTED", "material_caveats": self.valid_caveats}
        res = score_verification(output, self.f_01, True)
        self.assertEqual(res["caveat_retention"], 20)
        self.assertFalse(res["critical_fail"])

    def test_13_unrelated_caveat(self):
        output = {"verdict": "SUPPORTED", "material_caveats": ["This is a fake caveat", "Another fake caveat"]}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_14_missing_caveat(self):
        output = {"verdict": "SUPPORTED", "material_caveats": []}
        res = score_verification(output, self.f_01, True)
        self.assertTrue(res["critical_fail"])

    def test_15_scoring_component_totals(self):
        output = {
            "verdict": "SUPPORTED",
            "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}],
            "material_caveats": self.valid_caveats
        }
        res = score_verification(output, self.f_01, True)
        self.assertEqual(res["deterministic_total"], 100)
        self.assertEqual(res["verdict_correctness"], 30)
        self.assertFalse(res["critical_fail"])

    def test_16_bad_schema_points(self):
        output = {"wrong": "schema"}
        res = score_verification(output, self.f_01, False)
        self.assertEqual(res["schema_compliance"], 0)

    def test_17_input_ceiling(self):
        import benchmarks.model_selection.harness.runner as run_module
        req = {"track": "verification", "max_input_tokens": 100, "max_output_tokens": 100, "route_config": {"provider": "dummy", "model": "dummy"}}
        with self.assertRaises(TokenLimitExceeded):
            run_module.process_call(FakeProvider("INPUT_TOKEN_FAIL", {}), req, "F01", 1, 10.0, 0.0, {"smoke_test_call_cap_inr": 10.0}, {}, Path("tmp"))

    def test_18_budget_ceiling(self):
        import benchmarks.model_selection.harness.runner as run_module
        req = {"track": "verification", "max_input_tokens": 1000, "max_output_tokens": 100, "route_config": {"provider": "dummy", "model": "dummy"}}
        with self.assertRaises(BudgetExceeded):
            run_module.process_call(FakeProvider("BUDGET_FAIL", {}), req, "F01", 1, 100.0, 0.0, {"smoke_test_call_cap_inr": 9999999}, {}, Path("tmp"))

    def test_19_per_call_cap(self):
        import benchmarks.model_selection.harness.runner as run_module
        req = {"track": "verification", "max_input_tokens": 1000, "max_output_tokens": 100, "route_config": {"provider": "dummy", "model": "dummy"}}
        with self.assertRaises(BudgetExceeded):
            run_module.process_call(FakeProvider("BUDGET_FAIL", {}), req, "F01", 1, 9999999.0, 0.0, {"smoke_test_call_cap_inr": 10.0}, {}, Path("tmp"))

    def test_20_post_call_accounting(self):
        pass

    def test_21_repetition_ids(self):
        run_id = generate_individual_run_id("copy", "F01", "provider:model", 1)
        self.assertTrue(run_id.endswith("_R1"))

    def test_22_request_contract(self):
        config = {"verification": {"max_output_tokens": 100, "max_output_tokens_by_route": {}, "max_input_tokens": 1000}}
        req = build_request("verification", "FAKE_PROMPT", {"claim": "data"}, {}, {"provider": "A", "model": "B"}, config)
        self.assertEqual(req["system_prompt"], "FAKE_PROMPT")
        self.assertNotIn("gold", req["fixture"])

    def test_23_perfect_fake_run(self):
        session, calls = run_benchmark("PERFECT")
        self.assertEqual(len(calls), 90)
        valid_calls = sum(1 for c in calls if c["valid"])
        self.assertEqual(valid_calls, 90)
        cf_calls = sum(1 for c in calls if c["critical_fail"])
        self.assertEqual(cf_calls, 0)
        shutil.rmtree(Path(f"benchmarks/model_selection/results/{session}"))

    @patch("socket.socket")
    def test_24_network_blocked(self, mock_socket):
        mock_socket.side_effect = Exception("Network blocked")
        session, calls = run_benchmark("PERFECT")
        self.assertEqual(len(calls), 90)
        shutil.rmtree(Path(f"benchmarks/model_selection/results/{session}"))

    def test_25_artifacts_populated(self):
        session, calls = run_benchmark("PERFECT")
        out_dir = Path("benchmarks/model_selection/results") / session
        self.assertTrue(len(list((out_dir / "raw").glob("*.json"))) == 90)
        self.assertTrue(len(list((out_dir / "normalized").glob("*.json"))) == 90)
        self.assertTrue(len(list((out_dir / "scores").glob("*.json"))) == 90)
        shutil.rmtree(out_dir)

    def test_26_doctor_jsonschema(self):
        import benchmarks.model_selection.harness.__main__ as main_module
        with patch('sys.exit') as mock_exit:
            main_module.doctor()
            mock_exit.assert_not_called()
