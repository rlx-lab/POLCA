# KernelBench: Benchmark Setup & Running Guide

KernelBench is a benchmark for **CUDA kernel optimization**. Each task requires generating an optimized CUDA kernel for matrix multiplication. We optimize the kernel code using 3 algorithms across 16 matrix multiplication tasks.

---

## 1. Installation

```bash
cd Trace-Bench/KernelBench
bash install.sh
```

After installation, ensure `uv` is on your PATH and activate the environment:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
source .venv/bin/activate
```

### Environment variables

```bash
export MODEL="claude-3.7-sonnet"

# Anthropic-compatible endpoint
export TRACE_CUSTOMLLM_URL="custom-url"
export TRACE_CUSTOMLLM_API_KEY="custom-api-key"
export TRACE_DEFAULT_LLM_BACKEND="CustomLLM"
export TRACE_CUSTOMLLM_MODEL="claude-3.7-sonnet"

export GEMINI_API_KEY="your-gemini-api-key"
export WANDB_API_KEY="your-wandb-api-key"
```

### CUDA evaluation server

KernelBench requires a GPU evaluation server running on the target machine. Start it before running any experiments:

```bash
# Example: start a server with 5 GPUs
uv run python cuda_eval_server.py \
    --cuda-devices cuda:0 cuda:1 cuda:2 cuda:3 cuda:4 \
    --port 6000 &
```

---

## 2. Tasks

We optimize on **16 matrix multiplication tasks** (task indices 0–15).

---

## 3. Running Algorithms

All commands should be run from the **`Trace-Bench/KernelBench/`** directory.

### 3.1 POLCA

```bash
uv run my_process_agents/kernel_PS.py \
    --task-idx 2 \
    --num-steps 11 \
    --num-candidates 5 \
    --num-threads 1 \
    --num-proposals 1 \
    --log-frequency 1 \
    --test-frequency 1 \
    --algorithm PS_epsNet_Summarizer \
    --epsilon 0.02 \
    --use-wandb \
    --project-name "kernelbench-polca"
```

### 3.2 GEPA

```bash
uv run my_process_agents/kernel_gepa_per_iter.py \
    --task_idx 2 \
    --max_iterations 9 \
    --save_results
```

### 3.3 OpenEvolve

```bash
uv run my_process_agents/kernel_openevolve.py \
    --task_idx 2 \
    --max_iterations 50 \
    --num_workers 5 \
    --save_results \
    --run_num 3
```

---