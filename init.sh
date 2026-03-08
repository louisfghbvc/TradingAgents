#!/bin/bash
# init.sh - Setup environment for TradingAgents

set -e

echo "🔧 Initializing TradingAgents Environment..."

# 1. Check/Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment exists."
fi

# 2. Install Dependencies
echo "📦 Installing requirements..."
./venv/bin/pip install -r requirements.txt

# 3. Setup Git (if not already)
if [ ! -d ".git" ]; then
    echo "Initializing Git..."
    git init
fi

echo "✅ Initialization Complete. Run 'source venv/bin/activate' to use."
