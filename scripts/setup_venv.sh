#!/bin/bash

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

if [ ! -d "leetcode_env" ]; then
    python3 -m venv leetcode_env
fi

source leetcode_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

chmod +x scripts/*.sh
chmod +x scripts/*.py

git config alias.organize '!bash scripts/organize_with_venv.sh'
git config alias.setup-venv '!bash scripts/setup_venv.sh'

echo "Setup complete"
echo "Usage: git organize"
