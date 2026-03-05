#!/bin/bash
# =============================================================================
# POLCA — Setup Script
# Clones all algorithm and benchmark repos needed to reproduce paper results.
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║            POLCA — Repository Setup                        ║"
echo "║  Stochastic Generative Optimization with LLM               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ---------------------------------------------------------------------------
# Repository definitions: name -> git URL
# ---------------------------------------------------------------------------
declare -A REPOS=(
    # === Algorithm Repos ===
    ["Trace"]="https://github.com/xuanfeiren/Trace"
    ["gepa-repo"]="https://github.com/xuanfeiren/gepa-repo"
    ["dspy-repo"]="https://github.com/xuanfeiren/dspy-repo"
    ["openevolve"]="https://github.com/xuanfeiren/openevolve"

    # === Benchmark Repos ===
    ["hotpotqa"]="https://github.com/xuanfeiren/hotpotqa"
    ["Trace-Bench"]="https://github.com/xuanfeiren/Trace-Bench"
    ["tau-bench"]="https://github.com/xuanfeiren/tau-bench"
)

# ---------------------------------------------------------------------------
# Clone or update each repository
# ---------------------------------------------------------------------------
clone_or_update() {
    local name="$1"
    local url="$2"

    if [ -d "$name" ]; then
        echo "  ✓ $name — already cloned, pulling latest..."
        (cd "$name" && git pull --ff-only 2>/dev/null || echo "    ⚠ pull skipped (local changes or detached HEAD)")
    else
        echo "  ⏳ Cloning $name..."
        git clone "$url" "$name"
        echo "  ✓ $name — cloned successfully"
    fi
}

echo "📦 Cloning / updating repositories..."
echo ""

echo "── Algorithm Repos ──────────────────────────────────────────"
for repo in Trace gepa-repo dspy-repo openevolve; do
    clone_or_update "$repo" "${REPOS[$repo]}"
done

echo ""
echo "── Benchmark Repos ─────────────────────────────────────────"
for repo in hotpotqa Trace-Bench tau-bench; do
    clone_or_update "$repo" "${REPOS[$repo]}"
done

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ All repositories ready!"
echo ""
echo "Next steps:"
echo "  1. See README.md for the full algorithm × benchmark matrix"
echo "  2. Run:  python run.py --list           to see all experiments"
echo "  3. Run:  python run.py <bench> <algo>    to run an experiment"
echo "════════════════════════════════════════════════════════════════"
