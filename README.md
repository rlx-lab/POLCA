# POLCA: Stochastic Generative Optimization with LLM

This repository serves as the **central entry point** for reproducing the experimental results in the paper *POLCA: Stochastic Generative Optimization with LLM*.

We benchmark **3 algorithms** across **4 benchmarks**:

## Algorithms

| Algorithm | Description | Source Repo |
|-----------|-------------|-------------|
| **POLCA** | Stochastic generative optimization with LLM (ours) | [`Trace`](https://github.com/xuanfeiren/Trace) |
| **GEPA** | Genetic Evolution for Prompt Adaptation | [`gepa-repo`](https://github.com/xuanfeiren/gepa-repo) |
| **OpenEvolve** | LLM-driven evolutionary optimization | [`openevolve`](https://github.com/xuanfeiren/openevolve) |

## Benchmarks

| Benchmark | Domain | Source Repo |
|-----------|--------|-------------|
| **τ-bench** | Tool-agent-user interaction (agent optimization) | [`tau-bench`](https://github.com/xuanfeiren/tau-bench) |
| **HotpotQA** | Multi-hop question answering (prompt optimization) | [`hotpotqa`](https://github.com/xuanfeiren/hotpotqa) |
| **VeriBench** | Formal verification with Lean (code generation) | [`Trace-Bench/Veribench`](https://github.com/xuanfeiren/Trace-Bench/tree/main/Veribench) |
| **KernelBench** | CUDA kernel optimization (code generation) | [`Trace-Bench/KernelBench`](https://github.com/xuanfeiren/Trace-Bench/tree/main/KernelBench) |

## Experiment Matrix

|              | POLCA | GEPA | OpenEvolve |
|:-------------|:-----:|:----:|:----------:|
| **τ-bench**     | ✅ | ✅ | ✅ |
| **HotpotQA**    | ✅ | ✅ | ✅ |
| **VeriBench**   | ✅ | ✅ | ✅ |
| **KernelBench** | ✅ | ✅ | ✅ |

## Quick Start

### 1. Clone this repo and all dependencies

```bash
git clone https://github.com/rlx-lab/POLCA.git
cd POLCA
```

This clones all algorithm and benchmark repos into the current directory.

### 2. List available experiments

```bash
python run.py --list
```

### 3. Run an experiment

```bash
# Run POLCA on HotpotQA (run #1)
python run.py hotpotqa polca --run-num 1

# Run GEPA on HotpotQA (run #2)
python run.py hotpotqa gepa --run-num 2

# Run OpenEvolve on HotpotQA
python run.py hotpotqa openevolve

# Dry run (print command without executing)
python run.py tau-bench polca --dry-run
```

## Repository Structure

```
POLCA/                          ← you are here
├── README.md                   ← this file
├── setup.sh                    ← clones all dependency repos
├── run.py                      ← master CLI entry point
├── benchmarks/                 ← per-benchmark setup guides
│   ├── tau-bench.md
│   ├── hotpotqa.md
│   ├── veribench.md
│   └── kernelbench.md
│
├── Trace/                      ← POLCA algorithm (Trace framework)
├── gepa-repo/                  ← GEPA algorithm
├── openevolve/                 ← OpenEvolve algorithm
├── dspy-repo/                  ← DSPy framework (dependency)
│
├── hotpotqa/                   ← HotpotQA benchmark
│   └── prompt_opt/             ← optimization scripts for all 3 algorithms
├── tau-bench/                  ← τ-bench benchmark
│   └── my_processing_agents/   ← optimization scripts for all 3 algorithms
└── Trace-Bench/                ← Trace-Bench (contains VeriBench & KernelBench)
    ├── Veribench/
    └── KernelBench/
```

## Per-Benchmark Setup

Each benchmark has detailed setup instructions covering installation, environment variables, and how to run all 3 algorithms:

- **[τ-bench](benchmarks/tau-bench.md)** — Agent optimization on retail customer service tasks
- **[HotpotQA](benchmarks/hotpotqa.md)** — Prompt optimization for multi-hop QA
- **[VeriBench](benchmarks/veribench.md)** — Lean formal verification code generation
- **[KernelBench](benchmarks/kernelbench.md)** — CUDA kernel optimization

<!-- ## Citation

```bibtex
@article{polca2025,
  title={POLCA: Stochastic Generative Optimization with LLM},
  author={},
  year={2025}
} -->
```

## License

See individual repository licenses.
