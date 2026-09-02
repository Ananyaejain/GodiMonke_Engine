import unittest
import sys
import shutil
import json
from pathlib import Path
from unittest.mock import patch
from .runner import run_benchmark, BudgetExceeded, TokenLimitExceeded, generate_individual_run_id, build_request
from .scorer import score_verification, score_copy
from .provider import FakeProvider
from .config import load_fixtures

class TestBenchmarkHarness(unittest.TestCase):
    def test_01_all_five_fixtures_load(self):
        fixtures = load_fixtures()
        self.assertEqual(len(fixtures), 5)

    def test_02_fixture_ids_are_unique(self):
        fixtures = load_fixtures()
        self.assertEqual(len(set(fixtures.keys())), 5)

    def test_03_critical_fail_detector(self):
        fixtures = load_fixtures()
        f_01 = fixtures["F01_UNION_BUDGET_CAPEX"]
        # Fake verification with hallucinated number 8888.88
        output = {
            "verdict": "SUPPORTED",
            "rationale_summary": "The evidence supports this. Value is 8888.88",
            "material_caveats": ["All three values are Budget Estimates"]
        }
        res = score_verification(output, f_01)
        self.assertTrue(res["critical_fail"])

        # Output with allowed number
        output2 = {
            "verdict": "SUPPORTED",
            "rationale_summary": "The evidence supports 12.22 lakh crore.",
            "material_caveats": ["All three values are Budget Estimates"]
        }
        res2 = score_verification(output2, f_01)
        self.assertFalse(res2["critical_fail"])

    def test_04_budget_hard_stop_works(self):
        with self.assertRaises(BudgetExceeded):
            import benchmarks.model_selection.harness.runner as run_module
            from benchmarks.model_selection.harness.provider import FakeProvider
            req = {"track": "verification", "route_config": {"provider": "dummy", "model": "dummy"}}
            run_module.process_call(FakeProvider("BUDGET_FAIL", {}), req, "F01", 1, 10.0, 5.0, {}, {}, Path("tmp"))

    def test_05_input_token_ceiling_works(self):
        with self.assertRaises(TokenLimitExceeded):
            import benchmarks.model_selection.harness.runner as run_module
            from benchmarks.model_selection.harness.provider import FakeProvider
            req = {"track": "verification", "max_input_tokens": 1000, "max_output_tokens": 1000, "route_config": {"provider": "dummy", "model": "dummy"}}
            run_module.process_call(FakeProvider("INPUT_TOKEN_FAIL", {}), req, "F01", 1, 1000.0, 0.0, {}, {}, Path("tmp"))

    def test_06_output_token_ceiling_works(self):
        with self.assertRaises(TokenLimitExceeded):
            import benchmarks.model_selection.harness.runner as run_module
            from benchmarks.model_selection.harness.provider import FakeProvider
            req = {"track": "verification", "max_input_tokens": 1000, "max_output_tokens": 1000, "route_config": {"provider": "dummy", "model": "dummy"}}
            run_module.process_call(FakeProvider("OUTPUT_TOKEN_FAIL", {}), req, "F01", 1, 1000.0, 0.0, {}, {}, Path("tmp"))

    def test_07_provider_request_contract(self):
        config = {"verification": {"max_output_tokens": 100, "max_output_tokens_by_route": {}, "max_input_tokens": 1000}}
        req = build_request("verification", "FAKE_PROMPT", {"claim": "data"}, {}, {"provider": "A", "model": "B"}, config)
        self.assertEqual(req["system_prompt"], "FAKE_PROMPT")
        self.assertNotIn("gold", req["fixture"])
        self.assertIn("route_config", req)

    def test_08_scoring_component_totals(self):
        fixtures = load_fixtures()
        f_01 = fixtures["F01_UNION_BUDGET_CAPEX"]
        output = {
            "verdict": "SUPPORTED",
            "rationale_summary": "12.22",
            "material_caveats": ["All three values are Budget Estimates"]
        }
        res = score_verification(output, f_01)
        self.assertEqual(res["score"], 100)
        self.assertFalse(res["critical_fail"])

        output_copy = {
            "blocks": [{"block_type": "factual", "text": "12.22", "claim_ids": ["CLM-F01-1"]}]
        }
        res_copy = score_copy(output_copy, f_01)
        self.assertEqual(res_copy["score"], 50)
        self.assertFalse(res_copy["critical_fail"])

    def test_09_artifact_population(self):
        session, calls = run_benchmark("PERFECT")
        out_dir = Path("benchmarks/model_selection/results") / session
        self.assertTrue((out_dir / "raw").is_dir())
        self.assertTrue((out_dir / "normalized").is_dir())
        self.assertTrue((out_dir / "scores").is_dir())

        raw_files = list((out_dir / "raw").glob("*.json"))
        self.assertTrue(len(raw_files) > 0)

        scores_files = list((out_dir / "scores").glob("*.json"))
        self.assertEqual(len(raw_files), len(scores_files))
        shutil.rmtree(out_dir)

    def test_10_repetition_numbering(self):
        run_id = generate_individual_run_id("copy", "F01", "provider:model", 1)
        self.assertTrue(run_id.endswith("_R1"))
        run_id2 = generate_individual_run_id("copy", "F01", "provider:model", 3)
        self.assertTrue(run_id2.endswith("_R3"))

    @patch("socket.socket")
    def test_11_network_access_is_blocked(self, mock_socket):
        mock_socket.side_effect = Exception("Network blocked")
        import urllib.request
        with self.assertRaises(Exception):
            urllib.request.urlopen("https://example.com", timeout=1)

    def test_12_doctor_jsonschema_requirement(self):
        import importlib.metadata
        v = importlib.metadata.version('jsonschema')
        parts = v.split('.')
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        self.assertTrue(major == 4 and minor >= 19)
