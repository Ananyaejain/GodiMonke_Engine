import json
import os
from .http import safe_post
from .pricing import estimate_tokens, calculate_cost_usd, USD_INR_BUDGET_RATE
from ..provider import BenchmarkProvider

class DeepSeekProvider(BenchmarkProvider):
    def __init__(self, mode, model="deepseek-v4-flash"):
        self.mode = mode
        self.model = model
        self.route = f"deepseek:{self.model}"

    def _generate_payload(self, request, route_config):
        if "gold" in request["fixture"]:
            raise ValueError("Gold found in request fixture")
            
        sys_prompt = request["system_prompt"]
        fixture_json = json.dumps(request["fixture"])
        
        effort = "low" if "flash" in self.model else "high"
        
        payload = {
            "model": self.model,
            "instructions": sys_prompt,
            "input": fixture_json,
            "max_output_tokens": request["max_output_tokens"],
            "response_format": {
                "type": "json_schema",
                "schema": request["schema"]
            },
            "reasoning_effort": effort
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
        usage = response_json.get("usage", {})
        in_t = usage.get("input_tokens", 0)
        out_t = usage.get("output_tokens", 0)
        cached = usage.get("input_tokens_details", {}).get("cached_tokens", 0)
        reasoning = usage.get("output_tokens_details", {}).get("reasoning_tokens", 0)
        
        return {
            "output": response_json.get("choices", [{}])[0].get("message", {}).get("content"),
            "usage": {
                "input_tokens": in_t,
                "billed_output_tokens": out_t,
                "cached_tokens": cached,
                "reasoning_tokens": reasoning,
            }
        }
