import json
import os
from .http import safe_post, MissingCredential
from .pricing import estimate_tokens, calculate_cost_usd, USD_INR_BUDGET_RATE
from ..provider import BenchmarkProvider, UsageEstimate, ProviderIncompleteResponse


GEMINI_SUPPORTED_SCHEMA_KEYS = {
    "type", "format", "title", "description", "enum", "items", "prefixItems",
    "minItems", "maxItems", "minimum", "maximum", "anyOf", "oneOf",
    "properties", "additionalProperties", "required", "$id", "$defs",
    "$ref", "$anchor", "propertyOrdering"
}

import copy

def _project_gemini_schema(schema):
    if not isinstance(schema, dict):
        return schema

    projected = {}
    for k, v in schema.items():
        if k not in GEMINI_SUPPORTED_SCHEMA_KEYS:
            continue

        if k in ("properties", "$defs"):
            if isinstance(v, dict):
                projected[k] = {prop_name: _project_gemini_schema(prop_schema) for prop_name, prop_schema in v.items()}
        elif k in ("anyOf", "oneOf", "prefixItems"):
            if isinstance(v, list):
                projected[k] = [_project_gemini_schema(i) for i in v]
        elif k in ("items", "additionalProperties"):
            if isinstance(v, dict):
                projected[k] = _project_gemini_schema(v)
            else:
                projected[k] = copy.deepcopy(v)
        else:
            projected[k] = copy.deepcopy(v)

    return projected

class GoogleGeminiProvider(BenchmarkProvider):
    def __init__(self, mode, model="gemini-3.7-flash"):
        self.mode = mode
        self.model = model
        self.route = f"google:{self.model}"

    def get_headers(self):
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            raise MissingCredential("GEMINI_API_KEY is missing")
        return {"x-goog-api-key": key}

    def _generate_payload(self, request, route_config):
        if "gold" in request["fixture"]:
            raise ValueError("Gold found in request fixture")

        sys_prompt = request["system_prompt"]
        fixture_json = json.dumps(request["fixture"])

        payload = {
            "systemInstruction": {
                "parts": [{"text": sys_prompt}]
            },
            "contents": [{
                "role": "user",
                "parts": [{"text": fixture_json}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseJsonSchema": _project_gemini_schema(request["schema"]),
                "maxOutputTokens": request["max_output_tokens"],
                "thinkingConfig": {
                    "thinkingLevel": "medium"
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
        if not response_json.get("candidates"):
            raise ValueError("Provider normalization error: No candidates returned")
        candidate = response_json["candidates"][0]
        finish_reason = candidate.get("finishReason")
        if finish_reason != "STOP":
            raise ProviderIncompleteResponse(f"Gemini incomplete response. Reason: {finish_reason}")

        try:
            text = candidate["content"]["parts"][0]["text"]
            output = json.loads(text)
        except (KeyError, IndexError, TypeError):
            raise ValueError("Provider normalization error: Missing valid content parts")
        except json.JSONDecodeError:
            raise ValueError("Provider normalization error: Output is not valid JSON")

        usage = response_json.get("usageMetadata", {})
        in_t = usage.get("promptTokenCount", 0)
        cand_t = usage.get("candidatesTokenCount", 0)
        thought_t = usage.get("thoughtsTokenCount", 0)
        billed = cand_t + thought_t
        cached = usage.get("cachedContentTokenCount", 0)
        total = usage.get("totalTokenCount", 0)

        return {
            "output": output,
            "usage": {
                "input_tokens": in_t,
                "billed_output_tokens": billed,
                "cached_tokens": cached,
                "reasoning_tokens": thought_t,
                "total_tokens": total
            }
        }
