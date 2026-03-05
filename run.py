#!/usr/bin/env python3
"""
POLCA — Master Entry Point
===========================
Run any algorithm on any benchmark from a single CLI.

Usage:
    python run.py --list                            # Show all experiments
    python run.py hotpotqa polca                    # Run POLCA on HotpotQA
    python run.py hotpotqa gepa --run-num 3         # Run GEPA on HotpotQA (run #3)
    python run.py tau-bench openevolve              # Run OpenEvolve on tau-bench
    python run.py kernelbench polca                 # Run POLCA on KernelBench
    python run.py veribench gepa                    # Run GEPA on VeriBench

Algorithms:  polca | gepa | openevolve
Benchmarks:  hotpotqa | tau-bench | veribench | kernelbench
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Config: which algorithm × benchmark combinations are supported, and how
# ─────────────────────────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.abspath(__file__))

# Each entry maps (benchmark, algorithm) -> dict with:
#   repo_dir  : directory of benchmark repo (relative to ROOT)
#   cmd       : command template (list). {run_num} is substituted at runtime.
#   setup     : optional setup instructions
EXPERIMENTS = {
    # ── HotpotQA ─────────────────────────────────────────────────────────
    ("hotpotqa", "polca"): {
        "description": "POLCA (Trace PrioritySearch) on HotpotQA prompt optimization",
        "repo_dir": "hotpotqa",
        "cmd": ["bash", "prompt_opt/run_trace.sh", "{run_num}"],
        "setup": "cd hotpotqa && pip install -e . (or uv sync)",
    },
    ("hotpotqa", "gepa"): {
        "description": "GEPA optimizer on HotpotQA prompt optimization",
        "repo_dir": "hotpotqa",
        "cmd": ["bash", "prompt_opt/run_gepa.sh", "{run_num}"],
        "setup": "cd hotpotqa && pip install -e . (or uv sync)",
    },
    ("hotpotqa", "openevolve"): {
        "description": "OpenEvolve on HotpotQA prompt optimization",
        "repo_dir": "hotpotqa",
        "cmd": ["bash", "prompt_opt/run_openevolve.sh", "{run_num}"],
        "setup": "cd hotpotqa && pip install -e . (or uv sync)",
    },

    # ── tau-bench ────────────────────────────────────────────────────────
    ("tau-bench", "polca"): {
        "description": "POLCA agent optimization on tau-bench",
        "repo_dir": "tau-bench",
        "cmd": [
            "python", "my_processing_agents/tau_agent_opt.py",
            "--algorithm_name", "UCBAlgorithm",
            "--eval_frequency", "5",
            "--log_frequency", "1",
            "--num_epochs", "20",
            "--train_batch_size", "2",
            "--run_name", "polca-run-{run_num}",
        ],
        "setup": "cd tau-bench && pip install -e .",
    },
    ("tau-bench", "gepa"): {
        "description": "GEPA agent optimization on tau-bench",
        "repo_dir": "tau-bench",
        "cmd": [
            "python", "tau_trainer.py",
            "--algorithm_type", "gepa",
        ],
        "setup": "cd tau-bench && pip install -e .",
    },
    ("tau-bench", "openevolve"): {
        "description": "OpenEvolve agent optimization on tau-bench",
        "repo_dir": "tau-bench",
        "cmd": [
            "python", "tau_trainer.py",
            "--algorithm_type", "openevolve",
        ],
        "setup": "cd tau-bench && pip install -e .",
    },

    # ── VeriBench ────────────────────────────────────────────────────────
    ("veribench", "polca"): {
        "description": "POLCA on VeriBench (Lean formal verification)",
        "repo_dir": "Trace-Bench/Veribench",
        "cmd": ["bash", "run.sh", "{run_num}"],
        "setup": "cd Trace-Bench/Veribench && bash install.sh",
    },
    ("veribench", "gepa"): {
        "description": "GEPA on VeriBench (Lean formal verification)",
        "repo_dir": "Trace-Bench/Veribench",
        "cmd": ["bash", "my_processing_agents/run_gepa_direct_tasks_10_50.sh"],
        "setup": "cd Trace-Bench/Veribench && bash install.sh",
    },
    ("veribench", "openevolve"): {
        "description": "OpenEvolve on VeriBench (Lean formal verification)",
        "repo_dir": "Trace-Bench/Veribench",
        "cmd": ["bash", "run_openevolve.sh", "{run_num}"],
        "setup": "cd Trace-Bench/Veribench && bash install.sh",
    },

    # ── KernelBench ──────────────────────────────────────────────────────
    ("kernelbench", "polca"): {
        "description": "POLCA on KernelBench (CUDA kernel optimization)",
        "repo_dir": "Trace-Bench/KernelBench",
        "cmd": ["bash", "my_process_agents/run.sh", "{run_num}"],
        "setup": "cd Trace-Bench/KernelBench && bash install.sh",
    },
    ("kernelbench", "gepa"): {
        "description": "GEPA on KernelBench (CUDA kernel optimization)",
        "repo_dir": "Trace-Bench/KernelBench",
        "cmd": ["bash", "run_gepa.sh", "{run_num}"],
        "setup": "cd Trace-Bench/KernelBench && bash install.sh",
    },
    ("kernelbench", "openevolve"): {
        "description": "OpenEvolve on KernelBench (CUDA kernel optimization)",
        "repo_dir": "Trace-Bench/KernelBench",
        "cmd": ["bash", "run_openevolve.sh", "{run_num}"],
        "setup": "cd Trace-Bench/KernelBench && bash install.sh",
    },
}

# Canonical names & aliases
ALGORITHM_ALIASES = {
    "polca": "polca",
    "trace": "polca",
    "prioritysearch": "polca",
    "ps": "polca",
    "gepa": "gepa",
    "openevolve": "openevolve",
    "oe": "openevolve",
}

BENCHMARK_ALIASES = {
    "hotpotqa": "hotpotqa",
    "hotpot": "hotpotqa",
    "tau-bench": "tau-bench",
    "tau": "tau-bench",
    "taubench": "tau-bench",
    "veribench": "veribench",
    "veri": "veribench",
    "kernelbench": "kernelbench",
    "kernel": "kernelbench",
}

ALL_ALGORITHMS = ["polca", "gepa", "openevolve"]
ALL_BENCHMARKS = ["hotpotqa", "tau-bench", "veribench", "kernelbench"]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def resolve_alias(name, alias_map, kind):
    """Resolve a user-provided name through an alias map."""
    key = name.lower().strip()
    if key not in alias_map:
        valid = ", ".join(sorted(alias_map.keys()))
        print(f"❌ Unknown {kind}: '{name}'")
        print(f"   Valid options: {valid}")
        sys.exit(1)
    return alias_map[key]


def print_matrix():
    """Print the supported algorithm × benchmark matrix."""
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║             POLCA — Experiment Matrix                       ║")
    print("║  3 Algorithms × 4 Benchmarks                               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # Table header
    print(f"  {'Benchmark':<15s}  {'POLCA':<12s}  {'GEPA':<12s}  {'OpenEvolve':<12s}")
    print(f"  {'─'*15}  {'─'*12}  {'─'*12}  {'─'*12}")

    for bench in ALL_BENCHMARKS:
        row = f"  {bench:<15s}"
        for algo in ALL_ALGORITHMS:
            key = (bench, algo)
            if key in EXPERIMENTS:
                row += f"  {'✅':<12s}"
            else:
                row += f"  {'—':<12s}"
        print(row)

    print()
    print("Experiments:")
    print("─" * 70)
    for (bench, algo), info in sorted(EXPERIMENTS.items()):
        print(f"  {bench:<15s} × {algo:<12s}  →  {info['description']}")
    print()
    print("Usage:  python run.py <benchmark> <algorithm> [--run-num N]")
    print()


def check_repo_exists(repo_dir):
    """Check that the required repo directory is cloned."""
    full_path = os.path.join(ROOT, repo_dir)
    if not os.path.isdir(full_path):
        print(f"❌ Repository '{repo_dir}' not found at {full_path}")
        print(f"   Run: bash setup.sh   to clone all repos first.")
        sys.exit(1)
    return full_path


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="POLCA — run any algorithm on any benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "benchmark", nargs="?", type=str,
        help="Benchmark to run on (hotpotqa | tau-bench | veribench | kernelbench)"
    )
    parser.add_argument(
        "algorithm", nargs="?", type=str,
        help="Algorithm to run (polca | gepa | openevolve)"
    )
    parser.add_argument(
        "--run-num", type=int, default=1,
        help="Run number for reproducibility (default: 1)"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all supported experiments"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the command without executing it"
    )
    parser.add_argument(
        "--extra-args", nargs=argparse.REMAINDER, default=[],
        help="Extra arguments to pass through to the underlying script"
    )

    args = parser.parse_args()

    # --list mode
    if args.list:
        print_matrix()
        return

    # Require benchmark + algorithm
    if not args.benchmark or not args.algorithm:
        parser.print_help()
        print("\n💡 Tip: run `python run.py --list` to see all experiments")
        return

    benchmark = resolve_alias(args.benchmark, BENCHMARK_ALIASES, "benchmark")
    algorithm = resolve_alias(args.algorithm, ALGORITHM_ALIASES, "algorithm")

    key = (benchmark, algorithm)
    if key not in EXPERIMENTS:
        print(f"❌ No experiment defined for {benchmark} × {algorithm}")
        print(f"   Run `python run.py --list` to see supported combinations.")
        sys.exit(1)

    exp = EXPERIMENTS[key]
    repo_path = check_repo_exists(exp["repo_dir"])

    # Build command
    cmd = [
        c.replace("{run_num}", str(args.run_num))
        for c in exp["cmd"]
    ] + args.extra_args

    # Print header
    print()
    print("═" * 70)
    print(f"  POLCA — {exp['description']}")
    print(f"  Benchmark : {benchmark}")
    print(f"  Algorithm : {algorithm}")
    print(f"  Run #     : {args.run_num}")
    print(f"  Working dir: {repo_path}")
    print(f"  Command   : {' '.join(cmd)}")
    print(f"  Time      : {datetime.now().isoformat()}")
    print("═" * 70)
    print()

    if args.dry_run:
        print("🏜️  Dry run — not executing.")
        return

    # Execute
    result = subprocess.run(cmd, cwd=repo_path)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
