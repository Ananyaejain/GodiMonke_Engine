import json

SOURCE_ROLE_MAPPING = {
    "SUPPORTS": "SUPPORTS",
    "QUALIFIES": "QUALIFIES",
    "CONTEXT": "CONTEXT",
    "CONTRADICTS": "CONTRADICTS",
    "COUNTER_EVIDENCE": "CONTRADICTS",
    "CORROBORATION": "SUPPORTS",
    "ORIGINAL_STATEMENT": "CONTEXT"
}

class BenchmarkProvider:
    def estimate_usage(self, request, route_config):
        raise NotImplementedError
    def run_verification(self, request, route_config):
        raise NotImplementedError
    def run_copy(self, request, route_config):
        raise NotImplementedError

class FakeProvider(BenchmarkProvider):
    def __init__(self, mode):
        self.mode = mode

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
            "evidence_assessment": [],
            "material_caveats": [],
            "missing_evidence": [],
            "requires_human_review": False,
            "rationale_summary": "Based on the evidence, the claim is valid."
        }

        if "fixture" in request and "evidence" in request["fixture"]:
            ev = request["fixture"]["evidence"]
            if ev:
                output["evidence_assessment"] = [
                    {"source_id": e["source_id"], "assessment": SOURCE_ROLE_MAPPING.get(e.get("role", "SUPPORTS"), "SUPPORTS")} for e in ev
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
            fix = request.get("fixture", {})
            rs = fix.get("research_summary", "Valid")
            output["rationale_summary"] = rs
            output["material_caveats"] = [rs]

            output["evidence_assessment"] = []
            for ev in fix.get("evidence", []):
                role = ev.get("role", "SUPPORTS")
                assmt = SOURCE_ROLE_MAPPING.get(role, "SUPPORTS")
                output["evidence_assessment"].append({
                    "source_id": ev.get("source_id"),
                    "assessment": assmt
                })

        cost = 0.1
        if self.mode == "ACTUAL_COST_FAIL":
            cost = 15.0

        return {
            "output": output,
            "input_tokens": in_t,
            "output_tokens": out_t,
            "cached_tokens": 0,
            "cost_inr": cost,
            "retry_count": 0,
            "error_status": "OK"
        }

    def run_copy(self, request, route_config):
        in_t, out_t = self._get_base_tokens(request)

        fmt = request["fixture"].get("copy_format", "GM-SINGLE-01")
        output = {
            "format": fmt,
            "slides": [
                {
                    "slide_index": 1,
                    "role": "HOOK",
                    "headline": "A Great Post",
                    "body_blocks": [{"kind": "FACT", "text": "This is a fact.", "claim_ids": []}],
                    "commentary": "Interesting",
                    "mascot_direction": "Smiling"
                }
            ],
            "caption": "To conclude..."
        }

        if fmt == "GM-CAROUSEL-01" and self.mode == "PERFECT":
            output["slides"] = [
                {
                    "slide_index": i,
                    "role": "HOOK",
                    "headline": "A Great Post",
                    "body_blocks": [{"kind": "FACT", "text": "This is a fact.", "claim_ids": []}],
                    "commentary": "Interesting",
                    "mascot_direction": "Smiling"
                } for i in range(1, 4)
            ]

        if self.mode == "CRITICAL_FAIL":
            output["slides"][0]["body_blocks"][0]["text"] += " Number 8888.88."
            output["slides"][0]["body_blocks"][0]["claim_ids"] = []
        elif self.mode == "BAD_SCHEMA":
            output = {"bad": "schema"}
        elif self.mode == "PERFECT":
            lcs = request["fixture"].get("locked_claims", [])
            if lcs:
                for s in output["slides"]:
                    s["body_blocks"][0]["claim_ids"] = [lcs[0]["claim_id"]]
                    s["body_blocks"][0]["text"] = lcs[0]["text"]

        cost = 0.1
        if self.mode == "ACTUAL_COST_FAIL":
            cost = 15.0

        return {
            "output": output,
            "input_tokens": in_t,
            "output_tokens": out_t,
            "cached_tokens": 0,
            "cost_inr": cost,
            "retry_count": 0,
            "error_status": "OK"
        }
