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
    local branch="${3:-}"

    if [ -d "$name" ]; then
        echo "  ✓ $name — already cloned, pulling latest..."
        (cd "$name" && git pull --ff-only 2>/dev/null || echo "    ⚠ pull skipped (local changes or detached HEAD)")
    else
        echo "  ⏳ Cloning $name..."
        git clone "$url" "$name"
        if [ -n "$branch" ]; then
            (cd "$name" && git checkout "$branch")
        fi
        echo "  ✓ $name — cloned successfully"
    fi

    # If a specific branch is required, verify and switch if needed
    if [ -n "$branch" ] && [ -d "$name" ]; then
        current_branch=$(cd "$name" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
        if [ "$current_branch" != "$branch" ]; then
            echo "    ⚠ $name is on branch '$current_branch', switching to '$branch'..."
            (cd "$name" && git fetch origin && git checkout "$branch")
            echo "    ✓ $name now on branch '$branch'"
        else
            echo "    ✓ $name is on correct branch '$branch'"
        fi
    fi
}

echo "📦 Cloning / updating repositories..."
echo ""

echo "── Algorithm Repos ──────────────────────────────────────────"
clone_or_update "Trace" "${REPOS[Trace]}" "experimental"
for repo in gepa-repo dspy-repo openevolve; do
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
echo "  See README.md for the full algorithm × benchmark matrix"
echo "════════════════════════════════════════════════════════════════"
