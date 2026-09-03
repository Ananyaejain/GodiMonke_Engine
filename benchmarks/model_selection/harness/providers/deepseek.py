import json
import os
from .http import safe_post, MissingCredential
from .pricing import estimate_tokens, calculate_cost_usd, USD_INR_BUDGET_RATE
from ..provider import BenchmarkProvider, UsageEstimate, ProviderIncompleteResponse

class DeepSeekProvider(BenchmarkProvider):
    def __init__(self, mode, model="deepseek-v4-flash"):
        self.mode = mode
        self.model = model
        self.route = f"deepseek:{self.model}"

    def get_headers(self):
        key = os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            raise MissingCredential("DEEPSEEK_API_KEY is missing")
        return {"Authorization": f"Bearer {key}"}

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
            "reasoning": {
                "effort": effort
            },
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "verification_result",
                    "schema": request["schema"]
                }
            }
        }
        return payload

    def estimate_usage(self, request, route_config):
        payload = self._generate_payload(request, route_config)
        in_tokens = estimate_tokens(json.dumps(payload))
        out_tokens = request["max_output_tokens"]
        cost_usd = calculate_cost_usd(self.route, in_tokens, out_tokens)
        return UsageEstimate(in_tokens, out_tokens, cost_usd, cost_usd * USD_INR_BUDGET_RATE)

    def run_verification(self, request, route_config):
        if self.mode == "DRY_RUN":
            return self._dry_run(request, route_config)
        raise NotImplementedError("Live execution is explicitly disabled in B2A")

    def _dry_run(self, request, route_config):
        est_usage = self.estimate_usage(request, route_config)
        return {
            "output": None,
            "input_tokens": est_usage.estimated_input_tokens,
            "output_tokens": est_usage.max_output_tokens,
            "cached_tokens": 0,
            "reasoning_tokens": 0,
            "cost_usd": est_usage.estimated_cost_usd,
            "cost_inr": est_usage.estimated_cost_inr,
            "retry_count": 0,
            "error_status": "DRY_RUN"
        }

    def run_copy(self, request, route_config):
        if self.mode == "DRY_RUN":
            raise NotImplementedError("Copy track not supported in smoke test dry run.")
        raise NotImplementedError("Live execution is explicitly disabled in B2A")

    def parse_response(self, response_json):
        status = response_json.get("status")
        if status != "completed":
            reason = response_json.get("incomplete_details", {}).get("reason", "unknown")
            raise ProviderIncompleteResponse(f"DeepSeek incomplete response. Status: {status}, Reason: {reason}")

        try:
            outputs = response_json["output"]
            messages = [o for o in outputs if o.get("type") == "message"]
            if not messages:
                raise ValueError("No message block found")
            final_message = messages[-1]
            content = final_message.get("content", [])
            output_texts = [c for c in content if c.get("type") == "output_text"]
            if not output_texts:
                raise ValueError("No output_text block found")
            text = output_texts[-1]["text"]
            output = json.loads(text)
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"Provider normalization error: {e}")
        except json.JSONDecodeError:
            raise ValueError("Provider normalization error: Output is not valid JSON")

        usage = response_json.get("usage", {})
        in_t = usage.get("input_tokens", 0)
        out_t = usage.get("output_tokens", 0)
        cached = usage.get("input_tokens_details", {}).get("cached_tokens", 0)
        reasoning = usage.get("output_tokens_details", {}).get("reasoning_tokens", 0)
        total = usage.get("total_tokens", 0)
        
        return {
            "output": output,
            "usage": {
                "input_tokens": in_t,
                "billed_output_tokens": out_t,
                "cached_tokens": cached,
                "reasoning_tokens": reasoning,
                "total_tokens": total
            }
        }
