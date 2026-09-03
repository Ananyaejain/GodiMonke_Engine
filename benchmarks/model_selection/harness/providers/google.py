import json
import os
from .http import safe_post
from .pricing import estimate_tokens, calculate_cost_usd, USD_INR_BUDGET_RATE
from ..provider import BenchmarkProvider

class GoogleGeminiProvider(BenchmarkProvider):
    def __init__(self, mode, model="gemini-3.7-flash"):
        self.mode = mode
        self.model = model
        self.route = f"google:{self.model}"

    def _generate_payload(self, request, route_config):
        if "gold" in request["fixture"]:
            raise ValueError("Gold found in request fixture")
        
        sys_prompt = request["system_prompt"]
        fixture_json = json.dumps(request["fixture"])
        
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": sys_prompt + "\n\n" + fixture_json}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": request["schema"],
                "maxOutputTokens": request["max_output_tokens"],
                "thinkingConfig": {
                    "thinking": "MEDIUM"
                }
            }
        }
        return payload

    def estimate_usage(self, request, route_config):
        payload = self._generate_payload(request, route_config)
        in_tokens = estimate_tokens(json.dumps(payload))
        out_tokens = request["max_output_tokens"]
        cost_usd = calculate_cost_usd(self.route, in_tokens, out_tokens)
        return (in_tokens, out_tokens, cost_usd, cost_usd * USD_INR_BUDGET_RATE)

    def run_verification(self, request, route_config):
        if self.mode == "DRY_RUN":
            return self._dry_run(request, route_config)
        
        raise NotImplementedError("Live execution is explicitly disabled in B2A")
        
    def _dry_run(self, request, route_config):
        in_t, out_t, cost_usd, cost_inr = self.estimate_usage(request, route_config)
        return {
            "output": None,
            "input_tokens": in_t,
            "output_tokens": out_t,
            "cached_tokens": 0,
            "reasoning_tokens": 0,
            "cost_usd": cost_usd,
            "cost_inr": cost_inr,
            "retry_count": 0,
            "error_status": "DRY_RUN"
        }

    def run_copy(self, request, route_config):
        if self.mode == "DRY_RUN":
            raise NotImplementedError("Copy track not supported in smoke test dry run.")
        raise NotImplementedError("Live execution is explicitly disabled in B2A")

    def parse_response(self, response_json):
        usage = response_json.get("usageMetadata", {})
        in_t = usage.get("promptTokenCount", 0)
        cand_t = usage.get("candidatesTokenCount", 0)
        thought_t = usage.get("thoughtsTokenCount", 0)
        billed = cand_t + thought_t
        cached = usage.get("cachedContentTokenCount", 0)
        
        return {
            "output": response_json.get("candidates", [{}])[0].get("content", {}),
            "usage": {
                "input_tokens": in_t,
                "billed_output_tokens": billed,
                "cached_tokens": cached,
                "reasoning_tokens": thought_t,
            }
        }
