#!/bin/bash

# LeetCode Organizer with Virtual Environment

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "🚀 LeetCode Organizer (using venv)"
echo "Repository: $REPO_DIR"

# Check if virtual environment exists
if [ ! -d "leetcode_env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: git setup-venv"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source leetcode_env/bin/activate

# Run the organizer
echo "📁 Running organization..."
python3 scripts/simple_organizer.py "$REPO_DIR"

# Check for changes and commit
if [[ -n $(git status --porcelain) ]]; then
    echo ""
    echo "📋 Changes detected, committing..."

    git add .
    git commit -m "🤖 Auto-organized files by difficulty and problem number"
    git push origin main

    echo "✅ Changes committed and pushed!"
else
    echo "✅ Repository already organized!"
fi

echo "🎯 Organization complete!"