import json

class BenchmarkProvider:
    def estimate_usage(self, request, route_config):
        """Returns (estimated_input_tokens, max_output_tokens, estimated_cost_inr, estimated_cost_usd)"""
        raise NotImplementedError
    def run_verification(self, request, route_config):
        raise NotImplementedError
    def run_copy(self, request, route_config):
        raise NotImplementedError

class FakeProvider(BenchmarkProvider):
    def __init__(self, mode, fixtures_raw):
        self.mode = mode
        self.fixtures_raw = fixtures_raw

    def estimate_usage(self, request, route_config):
        if self.mode == "BUDGET_FAIL":
            return (500, request["max_output_tokens"], 99999.0, 1000.0)
        elif self.mode == "INPUT_TOKEN_FAIL":
            return (999999, request["max_output_tokens"], 0.1, 0.001)
        return (500, request["max_output_tokens"], 0.1, 0.001)

    def _get_base_tokens(self, request):
        if self.mode == "OUTPUT_TOKEN_FAIL":
            return 500, 999999
        return 500, 150

    def run_verification(self, request, route_config):
        in_t, out_t = self._get_base_tokens(request)

        output = {
            "verdict": "SUPPORTED",
            "confidence": 0.9,
            "evidence_assessment": [
                {
                    "source_id": "SRC-F01-A",
                    "assessment": "SUPPORTS"
                }
            ],
            "material_caveats": ["All three values are Budget Estimates for 2026-27, not actual realised expenditure."],
            "missing_evidence": [],
            "requires_human_review": False,
            "rationale_summary": "Based on the evidence, the claim is valid."
        }

        # Dynamically map evidence based on request fixture
        if "fixture" in request and "evidence" in request["fixture"]:
            ev = request["fixture"]["evidence"]
            if ev:
                output["evidence_assessment"] = [
                    {"source_id": e["source_id"], "assessment": "SUPPORTS"} for e in ev
                ]

        if self.mode == "CRITICAL_FAIL":
            output["rationale_summary"] += " The value is 8888.88."
        elif self.mode == "BAD_SCHEMA":
            output = {"wrong": "format"}
        elif self.mode == "INSUFFICIENT":
            output["verdict"] = "NOT_ESTABLISHED"
            output["rationale_summary"] = "Insufficient evidence."
            output["material_caveats"] = []

        if self.mode == "PERFECT":
            # Match actual gold verdict
            fix_text = request["fixture"].get("verification_claim", {}).get("text", "")
            for fid, f in self.fixtures_raw.items():
                if f.get("verification_claim", {}).get("text") == fix_text:
                    gold = f.get("gold", {})
                    if gold.get("verdict"):
                        output["verdict"] = gold["verdict"]
                    if gold.get("material_caveats"):
                        output["material_caveats"] = gold["material_caveats"]
                    break

        return {
            "output": output,
            "input_tokens": in_t,
            "output_tokens": out_t,
            "cached_tokens": 0,
            "cost_inr": 0.1,
            "retry_count": 0,
            "error_status": "OK"
        }

    def run_copy(self, request, route_config):
        in_t, out_t = self._get_base_tokens(request)

        output = {
            "format": request["fixture"].get("copy_format", "GM-SINGLE-01"),
            "slides": [
                {
                    "slide_index": 1,
                    "role": "HOOK",
                    "headline": "A Great Post",
                    "body_blocks": [
                        {
                            "kind": "FACT",
                            "text": "This is a fact.",
                            "claim_ids": []
                        }
                    ],
                    "commentary": "Interesting",
                    "mascot_direction": "Smiling"
                }
            ],
            "caption": "To conclude..."
        }

        if self.mode == "CRITICAL_FAIL":
            output["slides"][0]["body_blocks"][0]["text"] += " Number 8888.88."
            output["slides"][0]["body_blocks"][0]["claim_ids"] = []
        elif self.mode == "BAD_SCHEMA":
            output = {"bad": "schema"}
        elif self.mode == "PERFECT":
            fix_summary = request["fixture"].get("research_summary", "")
            for fid, f in self.fixtures_raw.items():
                if f.get("research_summary") == fix_summary:
                    lcs = f.get("locked_claims", [])
                    if lcs:
                        output["slides"][0]["body_blocks"][0]["claim_ids"] = [lcs[0]["claim_id"]]
                        output["slides"][0]["body_blocks"][0]["text"] = lcs[0]["text"]
                    break

        return {
            "output": output,
            "input_tokens": in_t,
            "output_tokens": out_t,
            "cached_tokens": 0,
            "cost_inr": 0.1,
            "retry_count": 0,
            "error_status": "OK"
        }
