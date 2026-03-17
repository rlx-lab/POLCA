# POLCA: Stochastic Generative Optimization with LLM

This repository serves as the **central entry point** for reproducing the experimental results in the paper [*POLCA: Stochastic Generative Optimization with LLM*](https://arxiv.org/abs/2603.14769).

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

### 2. Clone all dependency repos

```bash
bash setup.sh
```

### 3. Set up and run a benchmark

Each benchmark has its own `install.sh` and run scripts. See the [Per-Benchmark Setup](#per-benchmark-setup) section below.

```bash
# Example: HotpotQA
cd hotpotqa
bash install.sh
bash prompt_opt/run_trace.sh      # POLCA
bash prompt_opt/run_gepa.sh       # GEPA
bash prompt_opt/run_openevolve.sh # OpenEvolve
```

## Repository Structure

```
POLCA/                          ← you are here
├── README.md                   ← this file
├── setup.sh                    ← clones all dependency repos

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

