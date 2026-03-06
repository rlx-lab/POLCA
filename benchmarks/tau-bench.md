# τ-bench: Benchmark Setup & Running Guide

τ-bench is a benchmark for **Tool-Agent-User Interaction** in real-world domains (Airline and Retail customer service). We optimize the agent's tool descriptions and additional instructions to improve task completion rates.

**Paper**: [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)

---

## 1. Installation (uv — recommended)

The fastest way to set up τ-bench with all algorithm dependencies:

```bash
cd tau-bench
bash install.sh
```

This single command will:
1. Install [uv](https://docs.astral.sh/uv/) if not already present
2. Clone algorithm repos into `tau-bench/` as editable sources:
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

Before running any experiments, set your API keys:

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export WANDB_API_KEY="your-wandb-api-key"
```

---

## 2. Installation (manual — alternative)

<details>
<summary>Click to expand manual setup steps</summary>

If you prefer not to use `uv`, you can set up manually with conda + pip:

### 2.1 Create conda environment

```bash
conda create -n tau python=3.13 -c conda-forge -y
conda activate tau
```

### 2.2 Install τ-bench

```bash
git clone https://github.com/xuanfeiren/tau-bench.git
cd ./tau-bench
pip install -e .
```

### 2.3 Clone and install Trace (required for POLCA)

```bash
git clone https://github.com/xuanfeiren/Trace.git
cd ./Trace
git checkout experimental
pip install -e .
cd ..
```

> **Note**: The `experimental` branch contains the PrioritySearch features needed for τ-bench optimization.

### 2.4 Clone and install DSPy + GEPA (required for GEPA)

```bash
git clone https://github.com/xuanfeiren/dspy-repo.git
cd ./dspy-repo
pip install -e .
cd ..

git clone https://github.com/xuanfeiren/gepa-repo.git
cd ./gepa-repo
pip install -e .
cd ..
```

### 2.5 Clone and install OpenEvolve (required for OpenEvolve)

```bash
git clone https://github.com/xuanfeiren/openevolve.git
cd ./openevolve
pip install -e .
cd ..
```

### 2.6 Install remaining pip dependencies

```bash
pip install wandb datasets pandas scikit-learn scipy seaborn matplotlib graphviz pyyaml python-dotenv torch
```

</details>

---

## 3. Running Algorithms

All optimization scripts are in `my_processing_agents/`. Every script should be run from the **`tau-bench/`** directory.

### 3.1 POLCA (PrioritySearch)

**Script**: `my_processing_agents/optimize_tau_agent.py`

**What it optimizes**: Agent tool descriptions and additional instructions using PrioritySearch with Trace.

#### Debug run

```bash
python my_processing_agents/optimize_tau_agent.py \
    --num_train_samples 10 \
    --num_validate_samples 10 \
    --num_test_samples 10 \
    --batch_size 2 \
    --num_batches 1 \
    --num_steps 5 \
    --num_threads 20 \
    --num_candidates 2 \
    --score_function mean
```

#### Full run (paper configuration)

```bash
python my_processing_agents/optimize_tau_agent.py \
    --num_train_samples 115 \
    --num_validate_samples 115 \
    --num_test_samples 115 \
    --num_candidates 5 \
    --batch_size 2 \
    --num_batches 1 \
    --num_steps 101 \
    --num_threads 20 \
    --memory_update_frequency 0 \
    --num_eval_samples 1 \
    --test_frequency 10 \
    --log_frequency 1 \
    --num_proposals 1 \
    --epsilon 0.1 \
    --project_name tau-bench-115-tasks \
    --run_name eps0.1_summarizer-pass@1 \
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
| `--num_candidates` | Candidates to propose per step | 2 |
| `--num_threads` | Parallel evaluation threads | 20 |
| `--score_function` | Scoring: `mean`, `ucb`, or `time` | `mean` |
| `--epsilon` | Epsilon for EpsilonNet PrioritySearch | 0.0 |
| `--epsnetPS` | Enable EpsilonNet mode | `False` |
| `--use_summarizer` | Enable trajectory summarizer | `False` |
| `--ablation` | Enable ablation mode (required for `--epsnetPS`) | `False` |
| `--optoprime_version` | Optimizer version (`v1` or `v2`) | `v2` |
| `--model` | LLM model for the agent | `gemini-2.0-flash` |
| `--user_model` | LLM model for user simulator | `gemini-2.0-flash` |
| `--memory_update_frequency` | Short-term memory duration (0 = disabled) | 2 |
| `--test_frequency` | How often to run test evaluation | `None` |
| `--project_name` | WandB project name | `tau-bench-priority-search` |
| `--run_name` | WandB run name | `debug` |

---

### 3.2 GEPA

**Script**: `my_processing_agents/dspy_opt.py`

**What it optimizes**: Agent instructions using GEPA (Genetic Evolution for Prompt Adaptation) from DSPy.

#### Debug run

```bash
python my_processing_agents/dspy_opt.py \
    --num_samples 10 \
    --model gemini-2.0-flash \
    --max_metric_calls 200 \
    --num_threads 20 \
    --run_name "gepa-debug" \
    --project "tau-bench-gepa" \
    --log_dir "dspy_results/gepa_debug"
```

#### Full run (paper configuration)

```bash
python my_processing_agents/dspy_opt.py \
    --num_samples 50 \
    --model gemini-2.0-flash \
    --max_metric_calls 2000 \
    --num_threads 20 \
    --log_frequency 2 \
    --use_wandb \
    --run_name "gepa-full" \
    --project "tau-bench-gepa" \
    --log_dir "dspy_results/gepa_full"
```

#### Key parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num_samples` | Number of tasks to optimize on | 10 |
| `--model` | LLM model (`gemini-2.5-flash-lite` or `gemini-2.0-flash`) | `gemini-2.0-flash` |
| `--max_metric_calls` | Total evaluation budget for GEPA | 2000 |
| `--num_threads` | Parallel evaluation threads | 20 |
| `--log_frequency` | Save snapshots every N iterations | 2 |
| `--log_dir` | Directory for GEPA logs and snapshots | `dspy_results/gepa_Nov25` |
| `--use_wandb` | Enable WandB logging | `True` |
| `--project` | WandB project name | `debug-DSPy` |
| `--run_name` | WandB run name | `DSPy_GEPA` |

---

### 3.3 OpenEvolve

**Script**: `my_processing_agents/openevolve_tau_opt_with_feedback.py`

**What it optimizes**: Agent instructions using evolutionary optimization with rich per-task feedback.

#### Debug run

```bash
python my_processing_agents/openevolve_tau_opt_with_feedback.py \
    --num_train_samples 10 \
    --max_iterations 20 \
    --parallel_evaluations 10 \
    --model gemini-2.0-flash \
    --output_dir "results/openevolve_debug" \
    --run_name "oe-debug" \
    --project_name "tau-bench-openevolve"
```

#### Full run (paper configuration)

```bash
python my_processing_agents/openevolve_tau_opt_with_feedback.py \
    --num_train_samples 50 \
    --max_iterations 200 \
    --parallel_evaluations 10 \
    --model gemini-2.0-flash \
    --max_feedback_tasks 3 \
    --max_conversation_length 2000 \
    --output_dir "results/openevolve_full" \
    --run_name "oe-full" \
    --project_name "tau-bench-openevolve"
```

#### Key parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num_train_samples` | Number of training tasks | 10 |
| `--max_iterations` | Maximum evolution iterations | 200 |
| `--parallel_evaluations` | Parallel evaluations per iteration | 10 |
| `--num_workers` | Worker processes for parallel iterations | 1 |
| `--model` | LLM model for evolution | `gemini-2.0-flash` |
| `--max_feedback_tasks` | Number of worst tasks to show feedback for | 3 |
| `--max_conversation_length` | Max conversation length in feedback (chars) | 2000 |
| `--max_artifact_bytes` | Max artifact size in bytes | 20480 |
| `--output_dir` | Output directory for results | `results/openevolve_feedback` |
| `--config` | Path to custom YAML config | auto (feedback config) |
| `--run_name` | Run name for logging | auto (timestamp) |
| `--project_name` | Project name for logging | `tau-bench-feedback` |

---

## 4. Task Domain

All experiments run on the **Retail** domain (115 customer service tasks). The agent is a **tool-calling agent** that interacts with a simulated user and a set of retail tools (order lookup, returns, exchanges, etc.).

The optimization **does not change the agent's code** — it only modifies:
1. **Tool descriptions** — clarifying how tools should be used
2. **Additional instructions** — strategic guidance and best practices

---

## 5. Results & Logging

- All algorithms log to **WandB** by default. Set `--use_wandb` / `--project` / `--run_name` to configure.
- POLCA results are saved via WandB logger and optionally to `--save_path`.
- GEPA snapshots are saved to `--log_dir` every `--log_frequency` iterations.
- OpenEvolve results are saved to `--output_dir`, including the effective config, per-iteration logs, and the best program.

---

## 6. Evaluation

To evaluate a saved agent against the full task set:

```bash
python my_processing_agents/evaluate_custom_agents.py
```

Or evaluate predictions from a string:

```bash
python my_processing_agents/evaluate_from_str.py
```
