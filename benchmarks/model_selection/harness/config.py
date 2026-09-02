import json
from pathlib import Path
import copy

BASE_DIR = Path("benchmarks/model_selection")

def load_config():
    with open(BASE_DIR / "benchmark_config.example.json") as f:
        return json.load(f)

def load_schemas():
    with open(BASE_DIR / "schemas/verification_result.schema.json") as f:
        v_schema = json.load(f)
    with open(BASE_DIR / "schemas/copy_result.schema.json") as f:
        c_schema = json.load(f)
    return v_schema, c_schema

def load_fixtures():
    with open(BASE_DIR / "fixtures/fixture_index.json") as f:
        idx = json.load(f)
    fixtures = {}
    for entry in idx["fixtures"]:
        f_id = entry["fixture_id"]
        f_file = f_id + ".json"
        with open(BASE_DIR / "fixtures" / f_file) as f:
            fixtures[f_id] = json.load(f)
    return fixtures

def load_prompts():
    with open(BASE_DIR / "prompts/verification_system.md") as f:
        v_prompt = f.read()
    with open(BASE_DIR / "prompts/copy_system.md") as f:
        c_prompt = f.read()
    return v_prompt, c_prompt

def sanitize_fixture(fixture):
    sanitized = copy.deepcopy(fixture)
    keys_to_remove = ["gold", "human_gold_status", "human_review", "gold_verdict", "prohibited_claims"]
    for key in keys_to_remove:
        if key in sanitized:
            del sanitized[key]
    return sanitized

def recursive_leakage_check(data, keys_to_ban):
    if isinstance(data, dict):
        for k, v in data.items():
            if k in keys_to_ban:
                raise Exception(f"Gold leakage detected: {k}")
            recursive_leakage_check(v, keys_to_ban)
    elif isinstance(data, list):
        for item in data:
            recursive_leakage_check(item, keys_to_ban)

def verify_no_leakage(sanitized_fixture):
    banned = {"gold", "human_gold_status", "gold_verdict", "prohibited_claims"}
    recursive_leakage_check(sanitized_fixture, banned)
