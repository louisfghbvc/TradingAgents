#!/bin/bash
# ci.sh - Continuous Integration Script for TradingAgents
# Run this before pushing code or deploying!

set -e # Exit immediately if a command exits with a non-zero status.

echo "🚀 Starting CI Pipeline..."

# 1. Environment Check
echo "🔍 Checking Environment..."
if [ ! -d "venv" ]; then
    echo "❌ venv not found! Run ./init.sh first."
    exit 1
fi

# 2. Linting (Style Guardrail)
echo "🧹 Running Linter (Black)..."
./venv/bin/black --check . || {
    echo "⚠️ Code style issues found! Running auto-formatter..."
    ./venv/bin/black .
}

# 3. Unit & Integration Tests (Correctness Guardrail)
echo "🧪 Running Tests (Pytest)..."
# We need to install pytest first if not present
if ! ./venv/bin/pip show pytest > /dev/null; then
    echo "Installing pytest..."
    ./venv/bin/pip install pytest requests
fi

# Run tests
# We set PYTHONPATH so it can find the tradingagents module
export PYTHONPATH=$PYTHONPATH:$(pwd)
./venv/bin/pytest tests/ -v

echo "✅ CI Pipeline Passed! You are safe to deploy. 🚢"
