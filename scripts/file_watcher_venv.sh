#!/bin/bash

# Real-time File Watcher with Virtual Environment

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "👀 Starting LeetCode File Watcher (using venv)"

# Check if virtual environment exists
if [ ! -d "leetcode_env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: git setup-venv"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source leetcode_env/bin/activate

# Create file watcher script
cat > scripts/watch_files.py << 'EOF'
import time
import os
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileWatcher(FileSystemEventHandler):
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.cpp'):
            print(f"🔔 New file detected: {Path(event.src_path).name}")
            time.sleep(1)  # Wait for file to be written
            subprocess.run(['bash', 'scripts/organize_with_venv.sh'], cwd=self.repo_path)

if __name__ == "__main__":
    import sys
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."

    watcher = FileWatcher(repo_path)
    observer = Observer()

    daily_path = Path(repo_path) / "Daily Questions"
    daily_path.mkdir(exist_ok=True)

    observer.schedule(watcher, str(daily_path), recursive=False)
    observer.start()

    print(f"👀 Watching: {daily_path}")
    print("Drop .cpp files in 'Daily Questions' folder")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 File watcher stopped!")

    observer.join()
EOF

# Run the watcher
python3 scripts/watch_files.py "$REPO_DIR"