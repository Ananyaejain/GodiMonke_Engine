import sys
import argparse
from .tests import unittest, TestBenchmarkHarness
from .runner import run_benchmark
from .config import load_config, load_fixtures, load_schemas, load_prompts

def doctor():
    import sys
    import importlib.metadata
    from pathlib import Path
    import re

    try:
        installed_version = importlib.metadata.version("jsonschema")
    except importlib.metadata.PackageNotFoundError:
        print("Doctor checks failed: jsonschema is not installed.")
        sys.exit(1)

    print(f"jsonschema version: {installed_version}")

    req_file = Path("benchmarks/model_selection/requirements-benchmark.txt")
    if not req_file.exists():
        print("Doctor checks failed: requirements-benchmark.txt not found.")
        sys.exit(1)

    req_text = req_file.read_text().strip()
    match = re.search(r"jsonschema>=([\d\.]+),<([\d\.]+)", req_text)
    if not match:
        print("Doctor checks failed: Unable to parse jsonschema requirement string.")
        sys.exit(1)

    min_v, max_v = match.groups()

    def parse_ver(v):
        return tuple(map(int, v.split('.')))

    inst_v = parse_ver(installed_version)
    if not (parse_ver(min_v) <= inst_v < parse_ver(max_v)):
        print(f"Doctor checks failed: installed version {installed_version} does not satisfy {req_text}")
        sys.exit(1)

    try:
        config = load_config()
        fixtures = load_fixtures()
        assert len(fixtures) == 5, "Should have 5 fixtures"
        v_schema, c_schema = load_schemas()
        v_prompt, c_prompt = load_prompts()
        print("Doctor checks passed!")
    except Exception as e:
        print(f"Doctor checks failed: {e}")
        sys.exit(1)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fake", action="store_true", help="Run with fake provider")
    parser.add_argument("--fake-mode", default="PERFECT", help="Fake mode: PERFECT, CRITICAL_FAIL, BAD_SCHEMA, INSUFFICIENT")

    args, unknown = parser.parse_known_args(sys.argv[2:])

    if not args.fake:
        print("Only --fake is supported in B1")
        sys.exit(1)

    session_id, results = run_benchmark(args.fake_mode)
    print(f"Benchmark run complete. Mode: {args.fake_mode} | ID: {session_id}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "doctor":
            doctor()
        elif sys.argv[1] == "run":
            run()
        else:
            print("Unknown command")
    else:
        print("Specify doctor or run")
