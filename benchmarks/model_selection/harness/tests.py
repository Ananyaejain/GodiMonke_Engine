import unittest
import sys
import shutil
import json
from pathlib import Path
from unittest.mock import patch
from .runner import run_benchmark, BudgetExceeded, TokenLimitExceeded, BudgetAccountingError, generate_individual_run_id, build_request
from .scorer import score_verification, score_copy, validate_schema, extract_numbers
from .provider import FakeProvider
from .config import load_fixtures, load_schemas, sanitize_fixture

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
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertTrue(res["critical_fail"])

    def test_04_changed_number_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "value 13.22", "material_caveats": self.valid_caveats}
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertTrue(res["critical_fail"])

    def test_05_numeric_formatting_accepted(self):
        # 3.2 and 3.20 treated equivalent
        self.assertEqual(extract_numbers("3.2"), extract_numbers("3.20"))
        # 146195 / 146,195 / 1,46,195 equivalent
        self.assertEqual(extract_numbers("146195"), extract_numbers("146,195"))
        self.assertEqual(extract_numbers("1,46,195"), extract_numbers("146,195"))

    def test_06_invented_date_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "happened in 2099-01-01", "material_caveats": self.valid_caveats}
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertTrue(res["critical_fail"])

    def test_07_invented_quote_rejected(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "They said 'This is fake'", "material_caveats": self.valid_caveats}
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertTrue(res["critical_fail"])

    def test_08_unsupported_claim_id(self):
        output = {"format": "GM-SINGLE-01", "slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["FAKE-CLAIM"]}]}]}
        res = score_copy(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertTrue(res["critical_fail"])

    def test_09_unsupported_source_id(self):
        output = {"verdict": "SUPPORTED", "evidence_assessment": [{"source_id": "FAKE-SRC", "assessment": "SUPPORTS"}], "material_caveats": self.valid_caveats}
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertTrue(res["critical_fail"])

    def test_10_missing_caveat_not_critical(self):
        output = {"verdict": "SUPPORTED", "material_caveats": [], "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}]}
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertFalse(res["critical_fail"])
        self.assertEqual(res["caveat_retention"], 0)

    def test_11_unrelated_caveat_not_critical(self):
        output = {"verdict": "SUPPORTED", "material_caveats": ["This is a fake caveat"], "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}]}
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertFalse(res["critical_fail"])
        self.assertEqual(res["caveat_retention"], 0)

    def test_12_uncertainty_promoted_is_critical(self):
        output = {"verdict": "SUPPORTED", "rationale_summary": "This is 100% certain and a confirmed fact.", "material_caveats": self.valid_caveats}
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertTrue(res["critical_fail"])

    def test_13_wrong_role_loses_points(self):
        # SRC-F01-A should be SUPPORTS
        output = {"verdict": "SUPPORTED", "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "CONTRADICTS"}], "material_caveats": self.valid_caveats}
        res = score_verification(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertEqual(res["evidence_integrity"], 0)
        self.assertEqual(res["semantic_evidence_fidelity"], "NEEDS_HUMAN_SCORE")

    def test_14_semantic_scores_remain_human(self):
        output = {"format": "GM-SINGLE-01", "slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["CLM-F01-1"]}]}]}
        res = score_copy(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertEqual(res["semantic_factual_fidelity"], "NEEDS_HUMAN_SCORE")
        self.assertEqual(res["final_score"], "NEEDS_HUMAN_SCORE")

    def test_15_wrong_format_loses_template_points(self):
        # Format requested: GM-SINGLE-01, we provide GM-CAROUSEL-01
        output = {"format": "GM-CAROUSEL-01", "slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["CLM-F01-1"]}]}]}
        res = score_copy(output, sanitize_fixture(self.f_01), self.f_01.get("gold", {}), True)
        self.assertEqual(res["concision_template_fit"], 0)

    def test_16_carousel_slide_counts(self):
        f_car = dict(self.f_01)
        f_car["copy_format"] = "GM-CAROUSEL-01"
        # 1 slide -> 0 pts
        out1 = {"format": "GM-CAROUSEL-01", "slides": [{"body_blocks": [{"kind": "FACT", "text": "12.22", "claim_ids": ["CLM-F01-1"]}]}]}
        res1 = score_copy(out1, sanitize_fixture(f_car), f_car.get("gold", {}), True)
        self.assertEqual(res1["concision_template_fit"], 0)
        # 3 slides -> 10 pts
        out3 = {"format": "GM-CAROUSEL-01", "slides": [out1["slides"][0]] * 3}
        res3 = score_copy(out3, sanitize_fixture(f_car), f_car.get("gold", {}), True)
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
        from .scorer import get_allowed_facts
        from .config import sanitize_fixture
        f_leak = dict(self.f_01)
        f_leak["gold"] = dict(f_leak["gold"])
        f_leak["gold"]["material_caveats"] = ["This caveat contains hidden number 7777.77"]

        sanitized = sanitize_fixture(f_leak)
        allowed_nums, _, _, _, _ = get_allowed_facts(sanitized)
        self.assertNotIn(7777.77, allowed_nums)

        output = {"verdict": "SUPPORTED", "rationale_summary": "I am leaking 7777.77", "material_caveats": []}
        res = score_verification(output, sanitize_fixture(f_leak), f_leak.get("gold", {}), True)
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

    def test_24_supported_confirmed(self):
        f = dict(self.f_01)
        f["gold"] = dict(f["gold"])
        f["gold"]["verdict"] = "SUPPORTED"
        output = {"verdict": "SUPPORTED", "rationale_summary": "confirmed fact", "material_caveats": [], "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}]}
        res = score_verification(output, sanitize_fixture(f), f["gold"], True)
        self.assertFalse(res["critical_fail"])

    def test_25_misleading_certainty(self):
        f = dict(self.f_01)
        f["gold"] = dict(f["gold"])
        f["gold"]["verdict"] = "MISLEADING_WITHOUT_CONTEXT"
        output = {"verdict": "SUPPORTED", "rationale_summary": "100% certain", "material_caveats": [], "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}]}
        res = score_verification(output, sanitize_fixture(f), f["gold"], True)
        self.assertTrue(res["critical_fail"])

    def test_26_apostrophe_not_quote(self):
        from .scorer import extract_quotes
        text = "India's economy and government's estimate say nothing's wrong."
        self.assertEqual(extract_quotes(text), set())
        text2 = "They said 'This is fake' and \"Double fake\""
        self.assertEqual(extract_quotes(text2), {'This is fake', 'Double fake'})

    def test_27_evidence_duplicate_source(self):
        f = dict(self.f_01)
        # f_01 expects SRC-F01-A with SUPPORTS
        output = {"verdict": "SUPPORTED", "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}, {"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}], "material_caveats": []}
        res = score_verification(output, sanitize_fixture(f), f["gold"], True)
        self.assertEqual(res["evidence_integrity"], 0)

    def test_28_evidence_missing_source(self):
        f = dict(self.f_01)
        output = {"verdict": "SUPPORTED", "evidence_assessment": [], "material_caveats": []}
        res = score_verification(output, sanitize_fixture(f), f["gold"], True)
        self.assertEqual(res["evidence_integrity"], 0)

    def test_29_evidence_exact_source_set(self):
        f = dict(self.f_01)
        output = {"verdict": "SUPPORTED", "evidence_assessment": [{"source_id": "SRC-F01-A", "assessment": "SUPPORTS"}, {"source_id": "SRC-F01-B", "assessment": "SUPPORTS"}], "material_caveats": []}
        res = score_verification(output, sanitize_fixture(f), f["gold"], True)
        self.assertEqual(res["evidence_integrity"], 15)

    def test_30_config_budget_validation(self):
        from .config import validate_config_budget
        # Mocking or calling the validate function
        valid_cfg = {"global_budget_inr": 200, "per_call_hard_cap_inr": 5, "smoke_test_global_cap_inr": 10}
        validate_config_budget(valid_cfg)  # should not raise
        invalid_cfg = {"global_budget_inr": 200}
        with self.assertRaises(ValueError):
            validate_config_budget(invalid_cfg)

    def test_31_canonical_visible_fixture_boundary(self):
        # We ensure scorer is blind to gold and receives exactly the sanitized fixture
        import inspect
        from .scorer import score_verification, score_copy
        # Verify get_sanitized_for_extractor is completely removed
        with self.assertRaises(ImportError):
            from .scorer import get_sanitized_for_extractor

        # Verify signatures require visible_fixture and gold separately
        sig_v = inspect.signature(score_verification)
        self.assertIn("visible_fixture", sig_v.parameters)
        self.assertIn("gold", sig_v.parameters)

        sig_c = inspect.signature(score_copy)
        self.assertIn("visible_fixture", sig_c.parameters)
        self.assertIn("gold", sig_c.parameters)

    def test_32_google_payload_no_gold(self):
        from .providers.google import GoogleGeminiProvider
        from .config import sanitize_fixture
        p = GoogleGeminiProvider("DRY_RUN")
        req = {"system_prompt": "sys", "fixture": sanitize_fixture(self.f_01), "schema": {}, "max_output_tokens": 100}
        rc = {}
        payload = p._generate_payload(req, rc)
        self.assertNotIn("gold", payload["contents"][0]["parts"][0]["text"])
        self.assertEqual(payload["systemInstruction"]["parts"][0]["text"], "sys")
        self.assertEqual(payload["generationConfig"]["thinkingConfig"]["thinkingLevel"], "medium")
        self.assertNotIn("thinking", payload["generationConfig"])
        self.assertNotIn("temperature", payload["generationConfig"])

    def test_33_deepseek_payload_no_gold(self):
        from .providers.deepseek import DeepSeekProvider
        from .config import sanitize_fixture
        p = DeepSeekProvider("DRY_RUN")
        req = {"system_prompt": "sys", "fixture": sanitize_fixture(self.f_01), "schema": {"type": "object"}, "max_output_tokens": 100}
        rc = {}
        payload = p._generate_payload(req, rc)
        self.assertNotIn("gold", payload["input"])
        self.assertEqual(payload["text"]["format"]["type"], "json_schema")
        self.assertEqual(payload["text"]["format"]["name"], "verification_result")
        self.assertEqual(payload["text"]["format"]["schema"], {"type": "object"})
        self.assertNotIn("response_format", payload)
        self.assertNotIn("temperature", payload)
        self.assertNotIn("reasoning_effort", payload)

    def test_34_no_search_tools(self):
        from .providers.google import GoogleGeminiProvider
        from .providers.deepseek import DeepSeekProvider
        from .config import sanitize_fixture
        p1 = GoogleGeminiProvider("DRY_RUN")
        p2 = DeepSeekProvider("DRY_RUN")
        req = {"system_prompt": "sys", "fixture": sanitize_fixture(self.f_01), "schema": {}, "max_output_tokens": 100}
        rc = {}

        payload1 = p1._generate_payload(req, rc)
        self.assertNotIn("tools", payload1)

        payload2 = p2._generate_payload(req, rc)
        self.assertNotIn("tools", payload2)
        self.assertNotIn("web_search", payload2)

    def test_35_thinking_reasoning_levels(self):
        from .providers.google import GoogleGeminiProvider
        from .providers.deepseek import DeepSeekProvider
        from .config import sanitize_fixture
        req = {"system_prompt": "sys", "fixture": sanitize_fixture(self.f_01), "schema": {"type": "object"}, "max_output_tokens": 100}
        rc = {}

        g = GoogleGeminiProvider("DRY_RUN")
        pg = g._generate_payload(req, rc)
        self.assertEqual(pg["generationConfig"]["thinkingConfig"]["thinkingLevel"], "medium")

        d1 = DeepSeekProvider("DRY_RUN", "deepseek-v4-flash")
        pd1 = d1._generate_payload(req, rc)
        self.assertEqual(pd1["reasoning"]["effort"], "low")

        d2 = DeepSeekProvider("DRY_RUN", "deepseek-v4-pro")
        pd2 = d2._generate_payload(req, rc)
        self.assertEqual(pd2["reasoning"]["effort"], "high")

    def test_36_schema_sent(self):
        from .providers.google import GoogleGeminiProvider
        from .providers.deepseek import DeepSeekProvider
        from .config import sanitize_fixture
        req = {"system_prompt": "sys", "fixture": sanitize_fixture(self.f_01), "schema": {"type": "object"}, "max_output_tokens": 100}
        rc = {}

        g = GoogleGeminiProvider("DRY_RUN")
        pg = g._generate_payload(req, rc)
        self.assertEqual(pg["generationConfig"]["responseSchema"], {"type": "object"})

        d = DeepSeekProvider("DRY_RUN")
        pd = d._generate_payload(req, rc)
        self.assertEqual(pd["text"]["format"]["schema"], {"type": "object"})

    def test_37_38_39_http_safety(self):
        from .providers.http import safe_post, SafeHTTPError
        from unittest.mock import patch
        import urllib.error

        # Test missing host in allowlist
        with self.assertRaises(SafeHTTPError) as cm:
            safe_post("https://evil.com", {}, {})
        self.assertIn("not in allowlist", str(cm.exception))

        # Test redaction on URLError/HTTPError
        with patch('urllib.request.build_opener') as mock_opener:
            mock_open = mock_opener.return_value.open
            mock_open.side_effect = urllib.error.URLError("Failed to connect with secret SECRETDATA123")

            with self.assertRaises(SafeHTTPError) as cm_redact:
                safe_post("https://api.deepseek.com", {}, {"Authorization": "Bearer SECRETDATA123"})
            self.assertIn("***", str(cm_redact.exception))
            self.assertNotIn("SECRETDATA123", str(cm_redact.exception))

        # test too large request
        with self.assertRaises(SafeHTTPError) as cm_size:
            safe_post("https://api.deepseek.com", {"k": "v"*6000000}, {})
        self.assertIn("exceeds maximum allowed size", str(cm_size.exception))

    def test_40_usage_accounting(self):
        from .providers.google import GoogleGeminiProvider
        from .providers.deepseek import DeepSeekProvider

        g = GoogleGeminiProvider("DRY_RUN")
        g_mock_resp = {
            "candidates": [{"content": {"parts": [{"text": "{\"verdict\": \"ok\"}"}]}}],
            "usageMetadata": {
                "promptTokenCount": 100,
                "candidatesTokenCount": 50,
                "thoughtsTokenCount": 25,
                "cachedContentTokenCount": 0
            }
        }
        res_g = g.parse_response(g_mock_resp)
        self.assertEqual(res_g["usage"]["billed_output_tokens"], 75)
        self.assertEqual(res_g["usage"]["reasoning_tokens"], 25)

        d = DeepSeekProvider("DRY_RUN")
        d_mock_resp = {
            "output": [
                {"type": "reasoning", "content": [{"type": "text", "text": "thought"}]},
                {"type": "message", "content": [{"type": "output_text", "text": "{\"verdict\": \"ok\"}"}]}
            ],
            "usage": {
                "input_tokens": 10,
                "output_tokens": 75,
                "output_tokens_details": {"reasoning_tokens": 25}
            }
        }
        res_d = d.parse_response(d_mock_resp)
        self.assertEqual(res_d["usage"]["billed_output_tokens"], 75)
        self.assertEqual(res_d["usage"]["reasoning_tokens"], 25)

    def test_41_peak_pricing_preflight(self):
        from .providers.pricing import calculate_cost_usd
        # Flash: 0.44 input, 1.32 output
        c = calculate_cost_usd("deepseek:deepseek-v4-flash", 1000000, 1000000)
        self.assertAlmostEqual(c, 1.76) # 0.44 + 1.32

        c2 = calculate_cost_usd("deepseek:deepseek-v4-pro", 1000000, 1000000)
        self.assertAlmostEqual(c2, 5.28) # 1.32 + 3.96

    def test_42_local_token_estimator(self):
        from .providers.pricing import estimate_tokens
        text = "Hello world" # 11 chars
        self.assertEqual(estimate_tokens(text), 3) # 11 // 3

    def test_43_44_dry_run_invariant(self):
        from .runner import run_smoke
        calls = run_smoke(dry_run=True)
        self.assertEqual(len(calls), 3)
        for c in calls:
            self.assertEqual(c["track"], "verification")
            self.assertEqual(c["fixture"]["verification_claim"]["claim_id"], "CLM-F03-VERIFY")

    @patch("socket.socket")
    def test_45_network_block_live(self, mock_socket):
        # We explicitly block the socket but run_smoke dry run should still succeed because it doesn't use the network
        from .runner import run_smoke
        calls = run_smoke(dry_run=True)
        self.assertEqual(len(calls), 3)

    def test_46_missing_credential(self):
        from .providers.google import GoogleGeminiProvider
        from .providers.deepseek import DeepSeekProvider
        from .providers.http import MissingCredential
        import os

        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        if "DEEPSEEK_API_KEY" in os.environ:
            del os.environ["DEEPSEEK_API_KEY"]

        with self.assertRaises(MissingCredential):
            GoogleGeminiProvider("DRY_RUN").get_headers()

        with self.assertRaises(MissingCredential):
            DeepSeekProvider("DRY_RUN").get_headers()

        os.environ["GEMINI_API_KEY"] = "gem_test"
        h_gem = GoogleGeminiProvider("DRY_RUN").get_headers()
        self.assertEqual(h_gem["x-goog-api-key"], "gem_test")

        os.environ["DEEPSEEK_API_KEY"] = "ds_test"
        h_ds = DeepSeekProvider("DRY_RUN").get_headers()
        self.assertEqual(h_ds["Authorization"], "Bearer ds_test")

    def test_47_gemini_schema_projection(self):
        from .providers.google import GoogleGeminiProvider
        from .config import sanitize_fixture
        import copy

        original_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "maxLength": 100
                },
                "age": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 120
                }
            },
            "required": ["name"]
        }

        req = {
            "system_prompt": "sys",
            "fixture": sanitize_fixture(self.f_01),
            "schema": copy.deepcopy(original_schema),
            "max_output_tokens": 100
        }

        p = GoogleGeminiProvider("DRY_RUN")
        payload = p._generate_payload(req, {})
        gemini_schema = payload["generationConfig"]["responseSchema"]

        # Verify original intact
        self.assertIn("maxLength", req["schema"]["properties"]["name"])
        self.assertIn("$schema", req["schema"])

        # Verify stripped from projected
        self.assertNotIn("$schema", gemini_schema)
        self.assertNotIn("maxLength", gemini_schema["properties"]["name"])

        # Verify preserved
        self.assertEqual(gemini_schema["type"], "object")
        self.assertEqual(gemini_schema["properties"]["age"]["minimum"], 0)
        self.assertEqual(gemini_schema["properties"]["age"]["maximum"], 120)
        self.assertEqual(gemini_schema["required"], ["name"])

    def test_48_gemini_completion(self):
        from .providers.google import GoogleGeminiProvider
        from .provider import ProviderIncompleteResponse

        p = GoogleGeminiProvider("DRY_RUN")

        # STOP accepted
        stop_resp = {
            "candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": '{"ok": 1}'}]}}]
        }
        res = p.parse_response(stop_resp)
        self.assertEqual(res["output"]["ok"], 1)

        # MAX_TOKENS rejected
        max_resp = {
            "candidates": [{"finishReason": "MAX_TOKENS", "content": {"parts": [{"text": '{"ok": 1}'}]}}]
        }
        with self.assertRaises(ProviderIncompleteResponse) as cm:
            p.parse_response(max_resp)
        self.assertIn("MAX_TOKENS", str(cm.exception))

        # SAFETY rejected
        safe_resp = {
            "candidates": [{"finishReason": "SAFETY"}]
        }
        with self.assertRaises(ProviderIncompleteResponse) as cm2:
            p.parse_response(safe_resp)
        self.assertIn("SAFETY", str(cm2.exception))
        self.assertNotIn("SECRET", str(cm2.exception))

    def test_49_deepseek_completion(self):
        from .providers.deepseek import DeepSeekProvider
        from .provider import ProviderIncompleteResponse

        p = DeepSeekProvider("DRY_RUN")

        # Completed accepted
        ok_resp = {
            "status": "completed",
            "output": [
                {"type": "message", "content": [{"type": "output_text", "text": '{"ok": 1}'}]}
            ]
        }
        res = p.parse_response(ok_resp)
        self.assertEqual(res["output"]["ok"], 1)

        # Incomplete rejected
        inc_resp = {
            "status": "incomplete",
            "incomplete_details": {"reason": "max_output_tokens"},
            "output": []
        }
        with self.assertRaises(ProviderIncompleteResponse) as cm:
            p.parse_response(inc_resp)
        self.assertIn("max_output_tokens", str(cm.exception))
        self.assertIn("incomplete", str(cm.exception))
        self.assertNotIn("SECRET", str(cm.exception))

        # Failed rejected
        fail_resp = {
            "status": "failed",
            "incomplete_details": {"reason": "content_filter"}
        }
        with self.assertRaises(ProviderIncompleteResponse) as cm2:
            p.parse_response(fail_resp)
        self.assertIn("failed", str(cm2.exception))
        self.assertIn("content_filter", str(cm2.exception))

    def test_50_deepseek_final_message_and_reasoning(self):
        from .providers.deepseek import DeepSeekProvider

        p = DeepSeekProvider("DRY_RUN")

        resp = {
            "status": "completed",
            "output": [
                {"type": "reasoning", "content": [{"type": "text", "text": "secret thought"}]},
                {"type": "message", "content": [{"type": "output_text", "text": '{"wrong": 1}'}]},
                {"type": "reasoning", "content": [{"type": "text", "text": "more thought"}]},
                {"type": "message", "content": [{"type": "output_text", "text": '{"ok": 1}'}]}
            ]
        }
        res = p.parse_response(resp)
        self.assertEqual(res["output"], {"ok": 1})
        self.assertNotIn("thought", str(res))
