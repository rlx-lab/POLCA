# HotpotQA: Benchmark Setup & Running Guide

HotpotQA is a **multi-hop question answering** dataset. We optimize the prompt template used by an LLM to answer complex questions that require reasoning over multiple Wikipedia passages.

**Paper**: [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600)

---

## 1. Installation (uv — recommended)

```bash
cd hotpotqa
bash install.sh
```

This single command will:
1. Install [uv](https://docs.astral.sh/uv/) if not already present
2. Run `uv sync` to create a `.venv` and install all dependencies (including Trace, DSPy, GEPA, OpenEvolve from sibling repos)
3. Verify all imports

After installation, activate the environment:

```bash
source .venv/bin/activate
# or use uv run:
uv run python prompt_opt/trace_opt.py --help
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

All scripts are in `prompt_opt/` and should be run from the **`hotpotqa/`** directory. Each script accepts an optional `RUN_NUM` argument for multi-run experiments.

### 2.1 POLCA 

**Script**: `prompt_opt/run_trace.sh` → calls `prompt_opt/trace_opt.py`

**What it optimizes**: The prompt template for multi-hop QA using POLCA with Trace.

#### Quick start

```bash
bash prompt_opt/run_trace.sh         # default: run 1
bash prompt_opt/run_trace.sh 2       # run 2
```

#### Paper configuration (inside `run_trace.sh`)

```bash
uv run python prompt_opt/trace_opt.py \
    --num_train_samples 100 \
    --num_test_samples 100 \
    --num_candidates 5 \
    --batch_size 2 \
    --num_batches 1 \
    --num_steps 100 \
    --num_threads 10 \
    --num_eval_samples 5 \
    --log_frequency 1 \
    --algorithm PS_epsNet_Summarizer \
    --epsilon 0.1 \
    --project_name hotpotqa \
    --run_name run_1 \
    --output_dir prompt_opt/results/trace_1
```

#### Key parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num_train_samples` | Number of training examples | 10 |
| `--num_test_samples` | Number of test examples | 1 |
| `--num_candidates` | Candidates to propose per step | 5 |
| `--batch_size` | Examples per training batch | 2 |
| `--num_steps` | Number of optimization steps | 5 |
| `--num_threads` | Parallel evaluation threads | 20 |
| `--num_eval_samples` | Evaluation samples per candidate | 1 |
| `--epsilon` | Epsilon for EpsilonNet POLCA | 0.1 |
| `--project_name` | WandB project name | `hotpotqa-priority-search` |
| `--run_name` | WandB run name | `debug` |
| `--output_dir` | Output directory for results | — |

---

### 2.2 GEPA

**Script**: `prompt_opt/run_gepa.sh` → calls `prompt_opt/gepa_opt.py`

**What it optimizes**: The prompt template using GEPA (Genetic Evolution for Prompt Adaptation) from DSPy.

#### Quick start

```bash
bash prompt_opt/run_gepa.sh          # default: run 1
bash prompt_opt/run_gepa.sh 2        # run 2
```

#### Paper configuration (inside `run_gepa.sh`)

```bash
uv run python prompt_opt/gepa_opt.py \
    --num_tasks 100 \
    --num_val_tasks 100 \
    --max_metric_calls 2000 \
    --reflection_minibatch_size 10 \
    --num_threads 10 \
    --run_num 1 \
    --output_dir prompt_opt/results/gepa_1 \
    --log_dir prompt_opt/results/gepa_1/logs
```

#### Key parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num_tasks` | Number of training tasks | 100 |
| `--num_val_tasks` | Number of validation tasks | 100 |
| `--max_metric_calls` | Total evaluation budget for GEPA | 2000 |
| `--reflection_minibatch_size` | Minibatch size for reflection | 10 |
| `--num_threads` | Parallel evaluation threads | 10 |
| `--model` | LLM model for task execution | `gemini-2.5-flash-lite` |
| `--reflection_model` | LLM model for GEPA reflection | `gemini-2.5-flash-lite` |
| `--output_dir` | Output directory for results | `prompt_opt/results/gepa` |
| `--log_dir` | GEPA log directory | `prompt_opt/results/gepa/logs` |
| `--run_num` | Run number for tracking | 1 |

---

### 2.3 OpenEvolve

**Script**: `prompt_opt/run_openevolve.sh` → calls OpenEvolve's `openevolve-run.py`

**What it optimizes**: The prompt template using LLM-driven evolutionary optimization.

#### Quick start

```bash
bash prompt_opt/run_openevolve.sh    # default: run 1
bash prompt_opt/run_openevolve.sh 2  # run 2
```

#### Paper configuration (inside `run_openevolve.sh`)

```bash
uv run python ../openevolve/openevolve-run.py \
    prompt_opt/openevolve_initial_prompt.txt \
    prompt_opt/openevolve_opt.py \
    --config prompt_opt/openevolve_config.yaml \
    --output prompt_opt/results/openevolve_1 \
    --iterations 20
```

#### Key files

| File | Description |
|------|-------------|
| `prompt_opt/openevolve_initial_prompt.txt` | Initial prompt template (seed for evolution) |
| `prompt_opt/openevolve_opt.py` | Evaluation function for evolved prompts |
| `prompt_opt/openevolve_config.yaml` | OpenEvolve configuration (model, population, etc.) |

---

## 3. Task Domain

HotpotQA contains **multi-hop questions** that require reasoning over 2+ Wikipedia paragraphs. Each question has a gold answer and supporting facts.

The optimization changes **only the prompt template** — the LLM, retrieval mechanism, and evaluation pipeline remain fixed.

---

