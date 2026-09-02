import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from .config import load_config, load_fixtures, load_schemas, sanitize_fixture, verify_no_leakage
from .provider import FakeProvider
from .scorer import score_verification, score_copy, validate_schema

class TokenLimitExceeded(Exception):
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

def run_benchmark(mode="PERFECT"):
    config = load_config()
    fixtures = load_fixtures()
    v_schema, c_schema = load_schemas()

    budget = config["global_budget_inr"]
    spent = 0.0

    session_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_fake"
    out_dir = Path("benchmarks/model_selection/results") / session_id
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "raw").mkdir()
    (out_dir / "normalized").mkdir()
    (out_dir / "scores").mkdir()

    provider = FakeProvider(mode, fixtures)
    results = []

    for fixture_id, fixture in fixtures.items():
        sanitized = sanitize_fixture(fixture)
        verify_no_leakage(sanitized)

        for model_cfg in config["models"]:
            if not model_cfg.get("enabled", True):
                continue
            model_id = f"{model_cfg['provider']}:{model_cfg['model']}"

            for rep in range(config["repetitions"]):
                if spent >= budget:
                    break

                # VERIFICATION TRACK
                v_res = provider.run_verification(sanitized)
                if v_res["input_tokens"] > config["verification"]["max_input_tokens"]:
                    raise TokenLimitExceeded("Verification input token limit exceeded")
                if v_res["output_tokens"] > config["verification"]["max_output_tokens_by_route"].get(model_id, config["verification"]["max_output_tokens"]):
                    raise TokenLimitExceeded("Verification output token limit exceeded")

                spent += v_res["cost_inr"]
                v_valid = validate_schema(v_res["output"], v_schema)
                v_score = score_verification(v_res["output"], fixture.get("gold", {}))

                v_run_id = generate_individual_run_id("VERIFY", fixture_id, model_id, rep)

                # COPY TRACK
                c_res = provider.run_copy(sanitized)
                if c_res["input_tokens"] > config["copy"]["max_input_tokens"]:
                    raise TokenLimitExceeded("Copy input token limit exceeded")
                if c_res["output_tokens"] > config["copy"]["max_output_tokens_by_route"].get(model_id, config["copy"]["max_output_tokens"]):
                    raise TokenLimitExceeded("Copy output token limit exceeded")

                spent += c_res["cost_inr"]
                c_valid = validate_schema(c_res["output"], c_schema)
                c_score = score_copy(c_res["output"], fixture.get("gold", {}))

                c_run_id = generate_individual_run_id("COPY", fixture_id, model_id, rep)

                res = {
                    "fixture_id": fixture_id,
                    "model_id": model_id,
                    "rep": rep,
                    "v_run_id": v_run_id,
                    "c_run_id": c_run_id,
                    "v_valid": v_valid,
                    "c_valid": c_valid,
                    "v_critical_fail": v_score["critical_fail"],
                    "c_critical_fail": c_score["critical_fail"]
                }
                results.append(res)

    with open(out_dir / "summary.json", "w") as f:
        json.dump(results, f, indent=2)

    with open(out_dir / "summary.csv", "w") as f:
        f.write("fixture_id,model_id,rep,v_run_id,c_run_id,v_valid,c_valid,v_critical_fail,c_critical_fail\n")
        for r in results:
            f.write(f"{r['fixture_id']},{r['model_id']},{r['rep']},{r['v_run_id']},{r['c_run_id']},{r['v_valid']},{r['c_valid']},{r['v_critical_fail']},{r['c_critical_fail']}\n")

    with open(out_dir / "BENCHMARK_REPORT.md", "w") as f:
        f.write("# OFFLINE FAKE PROVIDER TEST\nNOT A REAL MODEL QUALITY RESULT\n")
        f.write(f"\nTotal spent: {spent} INR\n")
        f.write(f"Runs: {len(results)}\n")

    with open(out_dir / "run_manifest.json", "w") as f:
        json.dump({"session_id": session_id, "mode": mode, "models": len(config["models"]), "spent": spent}, f)

    return session_id, results
