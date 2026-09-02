import json

class BenchmarkProvider:
    def estimate_cost(self, request, route_config):
        raise NotImplementedError
    def run_verification(self, request, route_config):
        raise NotImplementedError
    def run_copy(self, request, route_config):
        raise NotImplementedError

class FakeProvider(BenchmarkProvider):
    def __init__(self, mode, fixtures_raw):
        self.mode = mode
        self.fixtures_raw = fixtures_raw

    def estimate_cost(self, request, route_config):
        if self.mode == "BUDGET_FAIL":
            return 99999.0
        return 0.1

    def _get_base_tokens(self, request):
        if self.mode == "INPUT_TOKEN_FAIL":
            return 999999, 10
        elif self.mode == "OUTPUT_TOKEN_FAIL":
            return 10, 999999
        return 500, 150

    def run_verification(self, request, route_config):
        in_t, out_t = self._get_base_tokens(request)

        output = {
            "verdict": "SUPPORTED",
            "confidence": "HIGH",
            "evidence_assessment": "The evidence perfectly supports this.",
            "material_caveats": ["This is a fake caveat."],
            "missing_evidence": [],
            "requires_human_review": False,
            "rationale_summary": "Based on the evidence, the claim is valid."
        }

        if self.mode == "CRITICAL_FAIL":
            # Add an invented number unsupported by evidence
            output["rationale_summary"] += " The value is 99999."
        elif self.mode == "BAD_SCHEMA":
            output = {"wrong": "format"}
        elif self.mode == "INSUFFICIENT":
            output["verdict"] = "NOT_ESTABLISHED"
            output["rationale_summary"] = "Insufficient evidence."
            output["material_caveats"] = []

        # To score perfectly in PERFECT mode:
        if self.mode == "PERFECT":
            # Grab the actual gold verdict
            fix_id = ""
            for fid, f in self.fixtures_raw.items():
                if f.get("verification_claim", {}).get("text") == request["fixture"].get("verification_claim", {}).get("text"):
                    fix_id = fid
                    break
            if fix_id:
                gold = self.fixtures_raw[fix_id].get("gold", {})
                if gold.get("verdict"):
                    output["verdict"] = gold["verdict"]
                if gold.get("material_caveats"):
                    output["material_caveats"] = gold["material_caveats"]

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
            "title": "A Great Post",
            "blocks": [
                {
                    "block_type": "factual",
                    "text": "This is a fact.",
                    "claim_ids": []
                }
            ],
            "conclusion": "To conclude..."
        }

        if self.mode == "CRITICAL_FAIL":
            # Add unsupported number 99999 and block without claim ID
            output["blocks"][0]["text"] += " Number 99999."
            output["blocks"][0]["claim_ids"] = [] # Factual block with no claim id
        elif self.mode == "BAD_SCHEMA":
            output = {"bad": "schema"}
        elif self.mode == "PERFECT":
            # Populate with allowed claims so it passes facts check
            fix_id = ""
            for fid, f in self.fixtures_raw.items():
                if f.get("research_summary") == request["fixture"].get("research_summary"):
                    fix_id = fid
                    break
            if fix_id:
                lcs = self.fixtures_raw[fix_id].get("locked_claims", [])
                if lcs:
                    output["blocks"][0]["claim_ids"] = [lcs[0]["claim_id"]]
                    output["blocks"][0]["text"] = lcs[0]["text"]

        return {
            "output": output,
            "input_tokens": in_t,
            "output_tokens": out_t,
            "cached_tokens": 0,
            "cost_inr": 0.1,
            "retry_count": 0,
            "error_status": "OK"
        }
