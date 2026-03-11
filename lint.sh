#!/bin/bash
# lint.sh - Code Style Guardrails

echo "🧹 Running Linters (Black)..."
# Check if black is installed
if ! command -v black &> /dev/null; then
    echo "Black not found, using venv..."
    ./venv/bin/black .
else
    black .
fi

echo "✨ Code Style Enforced!"
