# τ-bench: Benchmark Setup & Running Guide

τ-bench is a benchmark for **Tool-Agent-User Interaction** in real-world domains (Airline and Retail customer service). We optimize the agent's tool descriptions and additional instructions to improve task completion rates.

**Paper**: [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)

---

## 1. Installation (uv — recommended)

```bash
cd tau-bench
bash install.sh
```

This single command will:
1. Install [uv](https://docs.astral.sh/uv/) if not already present
2. Clone algorithm repos as editable sources:
   - `Trace` (branch `experimental`) — for POLCA
   - `dspy-repo` — for GEPA
   - `gepa-repo` — for GEPA
   - `openevolve` — for OpenEvolve
3. Run `uv sync` to create a `.venv` and install all dependencies
4. Verify all imports

After installation, activate the environment:

```bash
source .venv/bin/activate
# or use uv run:
uv run python my_processing_agents/optimize_tau_agent.py --help
```

To uninstall (remove `.venv` and build artifacts):

```bash
bash uninstall.sh
```

### Environment variables

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export WANDB_API_KEY="your-wandb-api-key"
```

---

## 2. Running Algorithms

All scripts are in `my_processing_agents/` and should be run from the **`tau-bench/`** directory.

### 2.1 POLCA

**Script**: `my_processing_agents/run_polca.sh` → calls `my_processing_agents/optimize_tau_agent.py`

**What it optimizes**: Agent tool descriptions and additional instructions using POLCA with Trace.

#### Quick start

```bash
bash my_processing_agents/run_polca.sh
```

#### Configuration (inside `run_polca.sh`)

```bash
uv run python my_processing_agents/optimize_tau_agent.py \
    --num_train_samples 10 \
    --num_validate_samples 10 \
    --num_test_samples 10 \
    --num_candidates 5 \
    --batch_size 2 \
    --num_batches 1 \
    --num_steps 101 \
    --num_threads 20 \
    --memory_update_frequency 0 \
    --num_eval_samples 10 \
    --log_frequency 1 \
    --num_proposals 1 \
    --project_name "tau-bench-polca" \
    --optoprime_version v2 \
    --ablation \
    --epsnetPS \
    --use_summarizer
```

#### Key parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num_train_samples` | Number of training tasks | 10 |
| `--num_validate_samples` | Number of validation tasks | 10 |
| `--num_test_samples` | Number of test tasks | 1 |
| `--batch_size` | Tasks per training batch | 2 |
| `--num_steps` | Number of optimization steps | 5 |
| `--num_candidates` | Candidates to propose per step | 5 |
| `--num_threads` | Parallel evaluation threads | 20 |
| `--num_eval_samples` | Evaluation samples per candidate | 1 |
| `--epsilon` | Epsilon for EpsilonNet POLCA | 0.1 |
| `--epsnetPS` | Enable EpsilonNet mode | `False` |
| `--use_summarizer` | Enable trajectory summarizer | `False` |
| `--project_name` | WandB project name | `tau-bench-priority-search` |
| `--run_name` | WandB run name | `debug` |

---

### 2.2 GEPA

**Script**: `my_processing_agents/run_gepa.sh` → calls `my_processing_agents/dspy_opt.py`

**What it optimizes**: Agent instructions using GEPA (Genetic Evolution for Prompt Adaptation) from DSPy.

#### Quick start

```bash
bash my_processing_agents/run_gepa.sh
```

#### Configuration (inside `run_gepa.sh`)

```bash
uv run python my_processing_agents/dspy_opt.py \
    --num_samples 10 \
    --model gemini-2.5-flash-lite \
    --max_metric_calls 2000 \
    --num_threads 20 \
    --log_frequency 2 \
    --log_dir "dspy_results/gepa_run"
```

#### Key parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num_samples` | Number of tasks to optimize on | 10 |
| `--model` | LLM model | `gemini-2.0-flash` |
| `--max_metric_calls` | Total evaluation budget for GEPA | 2000 |
| `--num_threads` | Parallel evaluation threads | 20 |
| `--log_frequency` | Save snapshots every N iterations | 2 |
| `--log_dir` | Directory for GEPA logs and snapshots | `dspy_results/gepa` |
| `--use_wandb` | Enable WandB logging | `False` |
| `--project` | WandB project name | `debug-DSPy` |
| `--run_name` | WandB run name | `DSPy_GEPA` |

---

### 2.3 OpenEvolve

**Script**: `my_processing_agents/run_openevolve.sh` → calls `my_processing_agents/openevolve_tau_opt_with_feedback.py`

**What it optimizes**: Agent instructions using evolutionary optimization with rich per-task feedback.

#### Quick start

```bash
bash my_processing_agents/run_openevolve.sh
```

#### Configuration (inside `run_openevolve.sh`)

```bash
uv run python my_processing_agents/openevolve_tau_opt_with_feedback.py \
    --num_train_samples 10 \
    --max_iterations 200 \
    --parallel_evaluations 10 \
    --num_workers 1 \
    --model "gemini-2.5-flash-lite" \
    --output_dir results/openevolve_feedback \
    --run_name run_1
```

#### Key parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num_train_samples` | Number of training tasks | 10 |
| `--max_iterations` | Maximum evolution iterations | 200 |
| `--parallel_evaluations` | Parallel evaluations per iteration | 10 |
| `--num_workers` | Worker processes | 1 |
| `--model` | LLM model for evolution | `gemini-2.0-flash` |
| `--max_feedback_tasks` | Number of worst tasks to show feedback for | 3 |
| `--max_conversation_length` | Max conversation length in feedback (chars) | 2000 |
| `--output_dir` | Output directory for results | `results/openevolve_feedback` |
| `--run_name` | Run name for logging | auto (timestamp) |
| `--project_name` | Project name for logging | `tau-bench-feedback` |

---

## 3. Task Domain

All experiments run on the **Retail** domain (115 customer service tasks). The agent is a **tool-calling agent** that interacts with a simulated user and a set of retail tools (order lookup, returns, exchanges, etc.).

The optimization **does not change the agent's code** — it only modifies:
1. **Tool descriptions** — clarifying how tools should be used
2. **Additional instructions** — strategic guidance and best practices

---
