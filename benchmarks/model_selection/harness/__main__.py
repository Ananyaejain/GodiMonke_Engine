import sys
import importlib.metadata
from pathlib import Path
import argparse

def doctor():
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
    parser.add_argument("command", choices=["doctor", "run", "live-doctor", "smoke"])
    parser.add_argument("--fake", action="store_true")
    parser.add_argument("--fake-mode", default="PERFECT")
    parser.add_argument("--dry-run", action="store_true")
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
    elif args.command == "live-doctor":
        from .runner import run_live_doctor
        run_live_doctor()
    elif args.command == "smoke":
        if not args.dry_run:
            print("ERROR: live execution disabled in B2A")
            sys.exit(1)
        from .runner import run_smoke
        run_smoke(dry_run=True)

if __name__ == "__main__":
    main()
