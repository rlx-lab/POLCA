# VeriBench: Benchmark Setup & Running Guide

VeriBench is a benchmark for **formal verification code generation** using Lean 4. Each task requires **translating a Python program into Lean 4 code**. Solutions are evaluated with a **3-step pipeline**: compilation, unit tests, and LLM-as-a-Judge.

**Paper**: [VeriBench: End-to-End Formal Verification Benchmark for AI Code Generation in Lean 4](https://openreview.net/pdf?id=rWkGFmnSNl)

**Dataset**: 41 easy-set tasks (task indices 10–50)

---

## 1. Installation (uv — recommended)

```bash
cd Trace-Bench/Veribench
bash install.sh
```

This single command will:
1. Install [uv](https://docs.astral.sh/uv/) if not already present
2. Run `uv sync` to create a `.venv` and install all dependencies (including Trace, DSPy, GEPA, OpenEvolve from `../../` sibling repos)
3. Verify all imports

After installation, activate the environment:

```bash
source .venv/bin/activate
# or use uv run:
uv run python my_processing_agents/solution_PS_withLLMjudge.py --help
```

To uninstall (remove `.venv` and build artifacts):

```bash
bash uninstall.sh
```

### Environment variables

VeriBench uses a **LiteLLM proxy** for LLM access. Set these before running:

```bash
# LiteLLM API Configuration



# Anthropic-compatible endpoint (used by some scripts)
export ANTHROPIC_API_BASE="your-api-base-url"
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# LiteLLM Model Configuration (we use claude-3.7-sonnet)
export TRACE_LITELLM_MODEL="model-name"

# Or if you use a custom LLM
export TRACE_CUSTOMLLM_URL="custom-url"
export TRACE_DEFAULT_LLM_BACKEND="CustomLLM"
export TRACE_CUSTOMLLM_MODEL="claude-3.7-sonnet"

# WandB (optional)
export WANDB_API_KEY="your-wandb-api-key"
```

---

## 2. Running Algorithms

All commands should be run from the **`Trace-Bench/Veribench/`** directory. Run all 3 algorithms at once:

```bash
bash my_processing_agents/scripts_with_LLM_judge.sh
```

Or run each algorithm individually:

### 2.1 POLCA

```bash
uv run python my_processing_agents/solution_PS_withLLMjudge.py \
    --task_idx 10 \
    --num_steps 20 \
    --num_threads 30 \
    --log_frequency 1 \
    --test_frequency 1 \
    --num_candidates 5 \
    --algorithm PS_epsNet_Summarizer \
    --epsilon 0.02 \
    --epsilon_for_summarizer 0.02 \
    --with_llm_judge \
    --use_wandb \
    --project_name "Veribench-POLCA"
```

### 2.2 GEPA

```bash
uv run python my_processing_agents/solution_GEPA_direct_with_LLMjudge.py \
    --task_idx 10 \
    --max_metric_calls 50 \
    --save_results \
    --run 1 \
    --log_dir results_llm_judge/gepa \
    --save_name gepa_1
```

### 2.3 OpenEvolve

```bash
uv run python my_processing_agents/solution_openevolve_with_LLMjudge.py \
    --task_idx 10 \
    --save_results
```

### Run all easy-set tasks (10–50)

```bash
for task_idx in $(seq 10 50); do
    # Replace the command below with any of the 3 algorithms above
    uv run python my_processing_agents/solution_PS_withLLMjudge.py \
        --task_idx $task_idx \
        --num_steps 20 --num_threads 30 --log_frequency 1 --test_frequency 1 \
        --num_candidates 5 --algorithm PS_epsNet_Summarizer \
        --epsilon 0.02 --epsilon_for_summarizer 0.02 \
        --with_llm_judge --use_wandb --project_name "Veribench-POLCA"
done
```

---
