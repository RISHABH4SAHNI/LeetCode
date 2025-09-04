#!/usr/bin/env python3
"""
Cleanup Script for LeetCode Repository
Removes duplicate files and organizes the repository structure
"""

import re
from pathlib import Path
from collections import defaultdict

def cleanup_duplicates(repo_path: str):
    """Remove duplicate files based on problem ID"""
    repo = Path(repo_path)

    folders = [
        repo / "Easy",
        repo / "Medium", 
        repo / "Hard"
    ]

    print("🧹 LeetCode Repository Cleanup Tool")
    print("=" * 50)

    problem_files = defaultdict(list)  # problem_id -> list of files

    # Collect all files by problem ID
    for folder in folders:
        if folder.exists():
            for file_path in folder.glob("*.cpp"):
                # Extract problem ID from filename
                match = re.match(r'^(\d+)_', file_path.name)
                if match:
                    problem_id = match.group(1)
                    problem_files[problem_id].append(file_path)

    # Find and handle duplicates
    duplicates_found = 0
    duplicates_removed = 0

    for problem_id, files in problem_files.items():
        if len(files) > 1:
            duplicates_found += 1
            print(f"\n📋 Problem #{problem_id} has {len(files)} copies:")

            for i, file_path in enumerate(files):
                size = file_path.stat().st_size
                mtime = file_path.stat().st_mtime
                print(f"   {i+1}. {file_path.relative_to(repo)} ({size} bytes)")

            # Keep the one with the shortest, most standard filename (or most recent)
            files_sorted = sorted(files, key=lambda f: (len(f.name), f.name))
            keep_file = files_sorted[0]

            print(f"   ✅ Keeping: {keep_file.relative_to(repo)}")

            # Remove duplicates
            for file_path in files[1:]:
                print(f"   🗑️  Removing: {file_path.relative_to(repo)}")
                file_path.unlink()
                duplicates_removed += 1

    print(f"\n📊 Cleanup Summary:")
    print(f"   • Found {duplicates_found} problems with duplicates")
    print(f"   • Removed {duplicates_removed} duplicate files")
    print(f"   ✅ Repository cleanup complete!")

if __name__ == "__main__":
    import sys
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    cleanup_duplicates(repo_path)