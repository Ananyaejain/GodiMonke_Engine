import os
import json
import uuid
import time
from datetime import datetime
from pathlib import Path
from .config import load_config, load_fixtures, load_schemas, load_prompts, sanitize_fixture, verify_no_leakage
from .provider import FakeProvider
from .scorer import score_verification, score_copy, validate_schema

class TokenLimitExceeded(Exception):
    pass

class BudgetExceeded(Exception):
    pass

class BudgetAccountingError(Exception):
    pass

def generate_individual_run_id(track, fixture_id, model_id, rep):
    if ":" in model_id:
        provider, model = model_id.split(":", 1)
        if model.startswith(provider):
            model = model[len(provider):]
            if model.startswith("-") or model.startswith("_"):
                model = model[1:]
        clean_model = f"{provider}_{model}".upper()
    else:
        clean_model = model_id.upper()
    clean_model = clean_model.replace(":", "_").replace("-", "_").replace(".", "_")
    return f"{track.upper()}_{fixture_id}_{clean_model}_R{rep}"

def build_request(track, prompt, fixture, schema, model_cfg, config):
    model_id = f"{model_cfg['provider']}:{model_cfg['model']}"
    max_out = config[track]["max_output_tokens_by_route"].get(model_id, config[track]["max_output_tokens"])

    return {
        "track": track,
        "system_prompt": prompt,
        "fixture": fixture,
        "schema": schema,
        "route_config": model_cfg,
        "max_output_tokens": max_out,
        "max_input_tokens": config[track]["max_input_tokens"]
    }

def process_call(provider, request, fixture_id, rep, budget, spent, config, fixture_gold, out_dir):
    est_in, max_out, est_cost_inr, est_cost_usd = provider.estimate_usage(request, request["route_config"])

    if est_in > request["max_input_tokens"]:
        raise TokenLimitExceeded(f"Estimated input tokens {est_in} > {request['max_input_tokens']}")

    per_call_cap = config["per_call_hard_cap_inr"]

    if est_cost_inr > per_call_cap:
        raise BudgetExceeded(f"Projected cost {est_cost_inr} exceeds per-call cap {per_call_cap}")

    if spent + est_cost_inr > budget:
        raise BudgetExceeded(f"Projected cost {est_cost_inr} exceeds remaining budget {budget - spent}")

    run_id = generate_individual_run_id(request["track"], fixture_id, f"{request['route_config']['provider']}:{request['route_config']['model']}", rep)

    start_time = time.time()
    if request["track"] == "verification":
        res = provider.run_verification(request, request["route_config"])
    else:
        res = provider.run_copy(request, request["route_config"])
    latency = (time.time() - start_time) * 1000.0

    actual_cost = res.get("cost_inr", 0.0)

    if actual_cost > per_call_cap:
        raise BudgetAccountingError(f"Actual cost {actual_cost} exceeds per-call cap {per_call_cap}")

    if actual_cost > est_cost_inr + 0.05: # Tolerance for rounding
        raise BudgetAccountingError(f"Actual cost {actual_cost} materially exceeds estimate {est_cost_inr}")

    spent += actual_cost

    if res["input_tokens"] > request["max_input_tokens"]:
        raise TokenLimitExceeded(f"Input tokens {res['input_tokens']} > {request['max_input_tokens']}")
    if res["output_tokens"] > request["max_output_tokens"]:
        raise TokenLimitExceeded(f"Output tokens {res['output_tokens']} > {request['max_output_tokens']}")

    if spent > budget:
        raise BudgetExceeded("Actual budget exceeded after call.")

    is_valid = validate_schema(res["output"], request["schema"])

    if request["track"] == "verification":
        score_res = score_verification(res["output"], request["fixture"], fixture_gold, is_valid)
    else:
        score_res = score_copy(res["output"], request["fixture"], fixture_gold, is_valid)

    with open(out_dir / "raw" / f"{run_id}.json", "w") as f:
        json.dump(res, f, indent=2)
    with open(out_dir / "normalized" / f"{run_id}.json", "w") as f:
        json.dump({"run_id": run_id, "output": res["output"]}, f, indent=2)
    with open(out_dir / "scores" / f"{run_id}.json", "w") as f:
        json.dump({"run_id": run_id, "score": score_res, "latency": latency, "cost": actual_cost}, f, indent=2)

    summary = {
        "run_id": run_id,
        "track": request["track"],
        "fixture_id": fixture_id,
        "provider": request["route_config"]["provider"],
        "model": request["route_config"]["model"],
        "rep": rep,
        "valid": is_valid,
        "critical_fail": score_res["critical_fail"],
        "input_tokens": res["input_tokens"],
        "output_tokens": res["output_tokens"],
        "cached_tokens": res.get("cached_tokens", 0),
        "latency_ms": latency,
        "cost_inr": actual_cost,
        "retry_count": res.get("retry_count", 0),
        "error_status": res.get("error_status", "OK")
    }
    if request["track"] == "verification":
        summary["score"] = score_res.get("deterministic_subtotal", 0)
    else:
        summary["score"] = score_res.get("deterministic_subtotal", 0)

    return summary, spent

def run_benchmark(mode="PERFECT"):
    config = load_config()
    fixtures = load_fixtures()
    v_schema, c_schema = load_schemas()
    v_prompt, c_prompt = load_prompts()

    budget = config.get("global_budget_inr", 200.0)
    spent = 0.0

    session_id = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{uuid.uuid4().hex[:6]}_{mode.lower()}"
    out_dir = Path("benchmarks/model_selection/results") / session_id
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "raw").mkdir(exist_ok=True)
    (out_dir / "normalized").mkdir(exist_ok=True)
    (out_dir / "scores").mkdir(exist_ok=True)

    provider = FakeProvider(mode)
    task_calls = []

    try:
        for fixture_id, fixture in fixtures.items():
            sanitized = sanitize_fixture(fixture)
            verify_no_leakage(sanitized)
            fixture_gold = fixture.get("gold", {})

            for model_cfg in config["models"]:
                if not model_cfg.get("enabled", True):
                    continue

                for rep in range(1, config["repetitions"] + 1):
                    v_req = build_request("verification", v_prompt, sanitized, v_schema, model_cfg, config)
                    v_sum, spent = process_call(provider, v_req, fixture_id, rep, budget, spent, config, fixture_gold, out_dir)
                    task_calls.append(v_sum)

                    c_req = build_request("copy", c_prompt, sanitized, c_schema, model_cfg, config)
                    c_sum, spent = process_call(provider, c_req, fixture_id, rep, budget, spent, config, fixture_gold, out_dir)
                    task_calls.append(c_sum)
    except BudgetExceeded as e:
        print(f"Benchmark stopped: {e}")
    except BudgetAccountingError as e:
        print(f"Post-call budget accounting error: {e}")
        if mode == "ACTUAL_COST_FAIL":
            raise e
    except TokenLimitExceeded as e:
        print(f"Token limit exceeded: {e}")
        if "TOKEN_FAIL" in mode:
            raise e

    with open(out_dir / "summary.json", "w") as f:
        json.dump(task_calls, f, indent=2)

    if task_calls:
        with open(out_dir / "summary.csv", "w") as f:
            headers = task_calls[0].keys()
            f.write(",".join(headers) + "\n")
            for r in task_calls:
                f.write(",".join(str(r[k]) for k in headers) + "\n")

    logical_pairs = len(task_calls) // 2

    with open(out_dir / "BENCHMARK_REPORT.md", "w") as f:
        f.write("# OFFLINE FAKE PROVIDER TEST\nNOT A REAL MODEL QUALITY RESULT\n")
        f.write(f"\nTotal spent: {spent} INR\n")
        f.write(f"Logical fixture/model/repetition pairs: {logical_pairs}\n")
        f.write(f"Provider task calls (verification + copy): {len(task_calls)}\n")

        sv_count = sum(1 for call in task_calls if call["valid"])
        cf_count = sum(1 for call in task_calls if call["critical_fail"])
        f.write(f"Schema-valid count: {sv_count}\n")
        f.write(f"Critical-failure count: {cf_count}\n")

    with open(out_dir / "run_manifest.json", "w") as f:
        json.dump({"session_id": session_id, "mode": mode, "models": len(config["models"]), "spent": spent}, f)

    return session_id, task_calls
