#!/bin/bash

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

if [ ! -d "leetcode_env" ]; then
    echo "Virtual environment not found! Run: git setup-venv"
    exit 1
fi

source leetcode_env/bin/activate
python3 scripts/simple_organizer.py "$REPO_DIR"

if [[ -n $(git status --porcelain) ]]; then
    git add .
    git commit -m "Auto-organized files by difficulty and problem number"
    git push origin main
    echo "Changes committed and pushed"
else
    echo "Repository already organized"
fi
