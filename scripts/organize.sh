#!/bin/bash

# Simple LeetCode Repository Organizer

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "🚀 LeetCode Simple Organizer"
echo "Repository: $REPO_DIR"
echo ""

# Run the organizer
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