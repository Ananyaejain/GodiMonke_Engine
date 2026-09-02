import sys
import importlib.metadata
from pathlib import Path
import argparse

def doctor():
    req_file = Path("benchmarks/model_selection/requirements-benchmark.txt")
    if req_file.exists():
        with open(req_file) as f:
            reqs = f.read()

    try:
        jsonschema_ver = importlib.metadata.version("jsonschema")
        print(f"jsonschema version: {jsonschema_ver}")
        parts = jsonschema_ver.split('.')
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        if major != 4 or minor < 19:
            print(f"Doctor checks failed: installed version {jsonschema_ver} does not satisfy jsonschema>=4.19,<5")
            sys.exit(1)
        else:
            print("Doctor checks passed!")
    except importlib.metadata.PackageNotFoundError:
        print("Doctor checks failed: jsonschema not installed.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["doctor", "run"])
    parser.add_argument("--fake", action="store_true")
    parser.add_argument("--fake-mode", default="PERFECT")
    args = parser.parse_args()

    if args.command == "doctor":
        doctor()
    elif args.command == "run":
        if args.fake:
            from .runner import run_benchmark
            session, calls = run_benchmark(args.fake_mode)
            print(f"Benchmark run complete. Mode: {args.fake_mode} | ID: {session}")
        else:
            print("Real API runs not permitted in this milestone.")
            sys.exit(1)

if __name__ == "__main__":
    main()
