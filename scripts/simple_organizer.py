#!/usr/bin/env python3
"""
Improved LeetCode Repository Organizer
- No cache creation
- Depends on commit message content
- Uses LeetCode API for accurate difficulty detection
- Organizes by difficulty with problem numbers
"""

import re
import shutil
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class ImprovedLeetCodeOrganizer:
    def __init__(self, repo_path: str, auto_mode: bool = False):
        self.repo_path = Path(repo_path)
        self.daily_path = self.repo_path / "Daily Questions"
        self.easy_path = self.repo_path / "Easy"
        self.medium_path = self.repo_path / "Medium"
        self.hard_path = self.repo_path / "Hard"
        self.auto_mode = auto_mode  # Process all files, not just recent ones

        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories"""
        for path in [self.daily_path, self.easy_path, self.medium_path, self.hard_path]:
            path.mkdir(exist_ok=True)

    def get_problem_difficulty_from_leetcode(self, problem_id: str) -> Optional[str]:
        """Get problem difficulty from LeetCode API using problem ID"""
        try:
            print(f"🔍 Querying LeetCode API for problem #{problem_id}...")
            
            # LeetCode GraphQL API
            url = "https://leetcode.com/graphql"
            query = """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
                ) {
                    questions: data {
                        questionId
                        questionFrontendId
                        title
                        difficulty
                    }
                }
            }
            """
            
            variables = {
                "categorySlug": "",
                "skip": 0,
                "limit": 50,
                "filters": {
                    "searchKeywords": problem_id
                }
            }
            
            payload = {"query": query, "variables": variables}
            
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
                'Referer': 'https://leetcode.com/problemset/all/'
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                questions = data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])
                
                # Find exact match by problem ID
                for question in questions:
                    if question.get('questionFrontendId') == problem_id:
                        difficulty = question.get('difficulty', '').upper()
                        print(f"✅ LeetCode API: Problem #{problem_id} → {difficulty}")
                        return difficulty
                
                print(f"⚠️ Problem #{problem_id} not found in search results")
            else:
                print(f"⚠️ LeetCode API returned status code: {response.status_code}")
            
            # Try alternative approach
            return self.get_problem_difficulty_alternative(problem_id)
            
        except Exception as e:
            print(f"⚠️ LeetCode API failed for #{problem_id}: {e}")
            return self.get_problem_difficulty_alternative(problem_id)
    
    def get_problem_difficulty_alternative(self, problem_id: str) -> Optional[str]:
        """Alternative method - fallback for common problems"""
        # Fallback for some well-known problems
        known_difficulties = {
            "1": "EASY",      # Two Sum
            "2": "MEDIUM",    # Add Two Numbers  
            "3": "MEDIUM",    # Longest Substring Without Repeating Characters
            "1317": "EASY",   # Convert Integer to the Sum of Two No-Zero Integers
            "3027": "HARD",   # Find the Number of Ways to Place People II
            "1304": "EASY",   # Find N Unique Integers Sum up to Zero
            "2749": "MEDIUM", # Minimum Operations to Make the Integer Zero
            "3495": "MEDIUM", # Minimum Operations to Make Array Elements Zero
        }
        
        if problem_id in known_difficulties:
            difficulty = known_difficulties[problem_id]
            print(f"✅ Known problem: #{problem_id} → {difficulty}")
            return difficulty
        
        print(f"❌ Could not determine difficulty for problem #{problem_id}")
        return None

    def get_commit_info_for_file(self, file_path: Path) -> Optional[Dict]:
        """Extract LeetCode problem info from git commit message"""
        try:
            import subprocess

            # Make file path relative to repo_path for git command
            try:
                relative_path = file_path.relative_to(self.repo_path)
            except ValueError:
                # If file_path is not under repo_path, use the full path
                relative_path = file_path

            print(f"🔍 Checking git log for: {relative_path}")

            # Get the most recent commit that modified this file
            result = subprocess.run([
                'git', 'log', '-n', '1', '--pretty=format:%s', '--follow', '--', str(relative_path)
            ], capture_output=True, text=True, cwd=self.repo_path)

            if result.returncode != 0:
                print(f"⚠️ Git command failed for {file_path.name}: {result.stderr}")
                return None

            commit_message = result.stdout.strip()
            print(f"📝 Found commit: '{commit_message}'")

            if not commit_message:
                print(f"⚠️ Empty commit message for {file_path.name}")
                return None

            return self.parse_commit_message(commit_message)

        except Exception as e:
            print(f"⚠️ Git commit analysis failed: {e}")
            return None

    def parse_commit_message(self, message: str) -> Optional[Dict]:
        """Parse commit message to extract LeetCode problem details"""
        
        # Common patterns in LeetCode commit messages
        patterns = [
            # Pattern 1: "Daily Question - 03:09:2025 3027. Find the Number of Ways to Place People II"
            r'(?:Daily Question.*?)(\d+)\.\s*(.+?)(?:\s*\((\w+)\))?$',
            
            # Pattern 2: "3027. Find the Number of Ways to Place People II (Medium)"
            r'(\d+)\.\s*(.+?)\s*\((\w+)\)',
            
            # Pattern 3: "Solved: 3027 - Find the Number of Ways to Place People II"
            r'(?:Solved:?\s*)(\d+)[\s\-]+(.+?)(?:\s*\((\w+)\))?$',
            
            # Pattern 4: "LeetCode 3027: Find the Number of Ways to Place People II"
            r'(?:LeetCode\s*)(\d+):\s*(.+?)(?:\s*\((\w+)\))?$',
        ]

        for i, pattern in enumerate(patterns, 1):
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                print(f"✅ Matched pattern {i}: {pattern}")
                problem_id = match.group(1)
                title = match.group(2).strip()
                commit_difficulty = match.group(3) if len(match.groups()) >= 3 and match.group(3) else None

                # Clean up title
                title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
                title = title.strip('. -')  # Remove trailing punctuation

                # Get accurate difficulty from LeetCode API
                print(f"🎯 Extracted from commit: #{problem_id} - {title}")
                api_difficulty = self.get_problem_difficulty_from_leetcode(problem_id)
                
                # Use API difficulty if available, otherwise use commit difficulty
                if api_difficulty:
                    difficulty = api_difficulty.capitalize()
                elif commit_difficulty:
                    difficulty = commit_difficulty.capitalize()
                    print(f"⚠️ Using commit difficulty for #{problem_id}: {difficulty}")
                else:
                    print(f"❌ No difficulty found for #{problem_id}")
                    return None

                result = {
                    'id': problem_id,
                    'title': title,
                    'difficulty': difficulty,
                    'source': 'commit_message'
                }

                print(f"✅ Final result: #{result['id']} - {result['title']} ({result['difficulty']})")
                return result

        print(f"❌ Could not parse commit message: '{message}'")
        print(f"📝 Tried {len(patterns)} patterns")
        return None

    def organize_file(self, file_path: Path) -> bool:
        """Organize a single file based on commit message and LeetCode API"""
        try:
            print(f"\n📂 Processing: {file_path.name}")
            print("="*50)

            # Extract problem info from git commit message
            problem_info = self.get_commit_info_for_file(file_path)

            if not problem_info:
                print(f"❌ Could not extract problem info from commit message")
                return False
            
            if not problem_info.get('difficulty'):
                print(f"❌ Could not determine difficulty for problem #{problem_info['id']}")
                return False

            # Check if this problem already exists in any difficulty folder
            existing_file = self.find_existing_problem(problem_info['id'])
            if existing_file:
                print(f"⚠️ Problem #{problem_info['id']} already exists: {existing_file}")
                return False

            # Determine target directory based on difficulty
            difficulty = problem_info['difficulty'].upper()
            if difficulty == 'EASY':
                target_dir = self.easy_path
            elif difficulty == 'MEDIUM':
                target_dir = self.medium_path
            elif difficulty == 'HARD':
                target_dir = self.hard_path
            else:
                print(f"❌ Unknown difficulty '{difficulty}', skipping file")
                return False

            # Create safe filename
            safe_title = re.sub(r'[^\\w\\s-]', '', problem_info['title']).replace(' ', '_')
            if len(safe_title) > 50:
                safe_title = safe_title[:50].rstrip('_')
            
            target_filename = f"{problem_info['id']}_{safe_title}.cpp"
            target_path = target_dir / target_filename

            # Copy file to appropriate difficulty folder
            if not target_path.exists():
                shutil.copy2(file_path, target_path)
                print(f"✅ Copied to: {difficulty} folder → {target_filename}")
                return True
            else:
                print(f"⚠️ File already exists: {target_filename}")
                return False

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
            return False

    def find_existing_problem(self, problem_id: str) -> Optional[Path]:
        """Check if a problem with the given ID already exists"""
        for folder in [self.easy_path, self.medium_path, self.hard_path]:
            if folder.exists():
                for existing_file in folder.glob(f"{problem_id}_*.cpp"):
                    return existing_file
        return None

    def organize_all(self):
        """Organize all files in Daily Questions folder"""
        print("🚀 Starting Improved LeetCode Organization...")
        print("📋 Extracting problem info from commit messages")
        print("🔍 Using LeetCode API for accurate difficulty detection")
        print("🚫 NO cache files will be created")

        # Get all cpp files in Daily Questions
        cpp_files = list(self.daily_path.glob("*.cpp"))
        
        if not cpp_files:
            print("\n⚠️ No .cpp files found in Daily Questions folder")
            return

        print(f"\n📁 Found {len(cpp_files)} files to process")

        organized = 0
        for file_path in cpp_files:
            if self.organize_file(file_path):
                organized += 1

        print(f"\n🎉 Organization complete!")
        print(f"✅ Successfully organized: {organized} files")
        print(f"📋 Total files processed: {len(cpp_files)}")

        # Show final distribution
        easy_count = len(list(self.easy_path.glob("*.cpp")))
        medium_count = len(list(self.medium_path.glob("*.cpp")))  
        hard_count = len(list(self.hard_path.glob("*.cpp")))

        print(f"\n📊 Final distribution:")
        print(f"   🟢 Easy: {easy_count} problems")
        print(f"   🟡 Medium: {medium_count} problems")
        print(f"   🔴 Hard: {hard_count} problems")
        print(f"   📈 Total: {easy_count + medium_count + hard_count} problems")

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Improved LeetCode Repository Organizer')
    parser.add_argument('repo_path', nargs='?', default='.', help='Path to the repository')
    parser.add_argument('--auto-mode', action='store_true', 
                       help='Process all files (for testing)')
    
    args = parser.parse_args()
    
    organizer = ImprovedLeetCodeOrganizer(args.repo_path, auto_mode=args.auto_mode)
    organizer.organize_all()
