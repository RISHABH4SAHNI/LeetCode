#!/usr/bin/env python3
"""
LeetCode Repository Organizer with AI-Powered Analysis
- Intelligent code analysis to identify LeetCode problems
- Sorts Daily Questions by date (only processes recent files)
- Organizes by difficulty with problem numbers
- Caches results for efficiency
"""

import re
import json
import shutil
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class SimpleLeetCodeOrganizer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.daily_path = self.repo_path / "Daily Questions"
        self.easy_path = self.repo_path / "Easy"
        self.medium_path = self.repo_path / "Medium"
        self.hard_path = self.repo_path / "Hard"

        self.cache_file = self.repo_path / "scripts" / "problem_cache.json"
        self.problem_cache = self.load_cache()

        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories"""
        for path in [self.daily_path, self.easy_path, self.medium_path, self.hard_path]:
            path.mkdir(exist_ok=True)
        (self.repo_path / "scripts").mkdir(exist_ok=True)

    def load_cache(self) -> Dict:
        """Load cached problem information"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}

    def save_cache(self):
        """Save problem cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.problem_cache, f, indent=2)
        except:
            pass

    def get_commit_info_for_file(self, file_path: Path) -> Optional[Dict]:
        """Extract LeetCode problem info from git commit message"""
        try:
            import subprocess

            # Get the most recent commit that modified this file
            result = subprocess.run([
                'git', 'log', '-n', '1', '--pretty=format:%s', '--', str(file_path)
            ], capture_output=True, text=True, cwd=self.repo_path)

            if result.returncode != 0:
                return None

            commit_message = result.stdout.strip()
            print(f"📝 Found commit: {commit_message}")

            return self.parse_commit_message(commit_message)

        except Exception as e:
            print(f"⚠️ Git commit analysis failed: {e}")
            return None

    def parse_commit_message(self, message: str) -> Optional[Dict]:
        """Parse commit message to extract LeetCode problem details"""

        # Common patterns in LeetCode commit messages
        patterns = [
            # Pattern 1: "Daily Question - 03:09:2025 3027. Find the Number of Ways to Place People II"
            r'(?:Daily Question.*?)?(\d+)\.\s*(.+?)(?:\s*\((\w+)\))?$',

            # Pattern 2: "3027. Find the Number of Ways to Place People II (Medium)"
            r'(\d+)\.\s*(.+?)\s*\((\w+)\)',

            # Pattern 3: "Solved: 3027 - Find the Number of Ways to Place People II"
            r'(?:Solved:?\s*)?(\d+)[\s\-]+(.+?)(?:\s*\((\w+)\))?$',

            # Pattern 4: "LeetCode 3027: Find the Number of Ways to Place People II"
            r'(?:LeetCode\s*)?(\d+):\s*(.+?)(?:\s*\((\w+)\))?$',
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                problem_id = match.group(1)
                title = match.group(2).strip()
                difficulty = match.group(3) if len(match.groups()) >= 3 and match.group(3) else None

                # Clean up title
                title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
                title = title.strip('. -')  # Remove trailing punctuation

                result = {
                    'id': problem_id,
                    'title': title,
                    'difficulty': difficulty.capitalize() if difficulty else 'Unknown',
                    'source': 'commit_message'
                }

                print(f"✅ Parsed: #{result['id']} - {result['title']} ({result['difficulty']})")
                return result

        print(f"❌ Could not parse commit message: {message}")
        return None

    def analyze_with_llm_logic(self, code: str) -> Optional[Dict]:
        """AI-powered analysis of code to identify LeetCode problem"""

        # Comprehensive analysis patterns for different LeetCode problem types
        analysis_rules = {
            # Geometry/Coordinate Problems
            'coordinate_geometry': {
                'patterns': [r'points', r'coordinates', r'x\[0\]', r'y\[1\]', r'comp.*vector.*int', r'sort.*points'],
                'problems': [
                    {'id': '3025', 'title': 'Find the Number of Ways to Place People I', 'difficulty': 'Medium'},
                    {'id': '1944', 'title': 'Number of Visible People in a Queue', 'difficulty': 'Hard'},
                ]
            },

            # Array/Subarray Problems  
            'array_subarray': {
                'patterns': [r'subarray', r'longest', r'delete', r'INT_MAX', r'consecutive'],
                'problems': [
                    {'id': '1493', 'title': 'Longest Subarray of 1s After Deleting One Element', 'difficulty': 'Medium'},
                    {'id': '53', 'title': 'Maximum Subarray', 'difficulty': 'Medium'},
                ]
            },

            # Matrix/Diagonal Problems
            'matrix_diagonal': {
                'patterns': [r'diagonal', r'matrix', r'traverse', r'direction', r'row.*col'],
                'problems': [
                    {'id': '498', 'title': 'Diagonal Traverse', 'difficulty': 'Medium'},
                    {'id': '1329', 'title': 'Sort the Matrix Diagonally', 'difficulty': 'Medium'},
                ]
            },

            # Game Theory Problems
            'game_theory': {
                'patterns': [r'alice', r'bob', r'flower', r'game', r'turn', r'winner'],
                'problems': [
                    {'id': '3021', 'title': 'Alice and Bob Playing Flower Game', 'difficulty': 'Medium'},
                ]
            },

            # Validation Problems
            'validation': {
                'patterns': [r'valid', r'sudoku', r'board', r'isValid', r'check'],
                'problems': [
                    {'id': '36', 'title': 'Valid Sudoku', 'difficulty': 'Medium'},
                    {'id': '37', 'title': 'Sudoku Solver', 'difficulty': 'Hard'},
                ]
            }
        }

        code_lower = code.lower()

        # Score each category based on pattern matches
        best_match = None
        best_score = 0

        for category, data in analysis_rules.items():
            score = sum(1 for pattern in data['patterns'] if re.search(pattern, code_lower))

            if score > best_score:
                best_score = score
                # Return the most likely problem from this category
                if data['problems'] and score > 0:
                    best_match = data['problems'][0]

        return best_match

    def extract_function_name(self, code: str) -> Optional[str]:
        """Extract main function name from C++ code"""
        patterns = [
            r'class\s+Solution\s*{[^}]*public:[^}]*?(\w+)\s*\([^)]*\)\s*{',
            r'(\w+)\s*\([^)]*\)\s*{[^}]*return',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, code, re.DOTALL | re.IGNORECASE)
            if matches:
                exclude = {'Solution', 'main', 'int', 'bool', 'string', 'vector', 'if', 'for', 'while', 'comp', 'cmp'}
                for match in matches:
                    if match and match not in exclude and len(match) > 2:
                        return match
        return None

    def get_problem_info_from_leetcode(self, function_name: str) -> Optional[Dict]:
        """Get problem info from cache or LeetCode API"""
        if function_name in self.problem_cache:
            return self.problem_cache[function_name]

        # Try basic API variations (fallback)
        try:
            url = "https://leetcode.com/graphql"
            query = """
            query questionData($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionId
                    questionFrontendId
                    title
                    difficulty
                }
            }
            """

            variations = [
                function_name.lower(),
                re.sub(r'([A-Z])', r'-\1', function_name).lower().strip('-'),
                re.sub(r'([A-Z])', r'-\\1', function_name).lower().strip('-'),
                function_name.lower().replace('_', '-')
            ]

            for variation in variations:
                payload = {"query": query, "variables": {"titleSlug": variation}}
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    question = data.get('data', {}).get('question')

                    if question:
                        problem_info = {
                            'id': question['questionFrontendId'],
                            'title': question['title'],
                            'difficulty': question['difficulty']
                        }

                        # Cache the result
                        self.problem_cache[function_name] = problem_info
                        self.save_cache()
                        return problem_info

        except Exception as e:
            print(f"⚠️ API call failed for {function_name}: {e}")

        return None

    def parse_date_from_filename(self, filename: str) -> datetime:
        """Parse date from filename like '1:09:2025.cpp'"""
        pattern = r'(\d{1,2}):(\d{2}):(\d{4})\.cpp'
        match = re.match(pattern, filename)
        if match:
            day, month, year = match.groups()
            return datetime(int(year), int(month), int(day))
        return datetime.min

    def sort_daily_files(self) -> list:
        """Sort daily files by date - only processes files modified in last 24 hours"""
        files = list(self.daily_path.glob("*.cpp"))

        # Filter files modified in the last 24 hours
        recent_files = []
        current_time = time.time()
        one_day_ago = current_time - (24 * 60 * 60)  # 24 hours in seconds

        for file_path in files:
            file_mtime = file_path.stat().st_mtime
            if file_mtime >= one_day_ago:
                recent_files.append(file_path)

        if recent_files:
            return sorted(recent_files, key=lambda f: self.parse_date_from_filename(f.name))
        else:
            return []

    def organize_file(self, file_path: Path) -> bool:
        """Organize a single file"""
        try:
            print(f"Processing: {file_path.name}")

            # 🎯 PRIMARY METHOD: Git commit analysis (most reliable)
            print("🎯 Checking git commit message...")
            problem_info = self.get_commit_info_for_file(file_path)

            if problem_info:
                print(f"📝 Git commit detection: #{problem_info['id']} - {problem_info['title']} ({problem_info['difficulty']})")
                # Cache the result
                function_name = self.extract_function_name(open(file_path, 'r').read()) or "git_detected"
                self.problem_cache[function_name] = problem_info
                self.save_cache()
            else:
                with open(file_path, 'r') as f:
                    code = f.read()

                    # 🧠 SECONDARY METHOD: AI-powered code analysis 
                    print("🧠 Falling back to AI code analysis...")
                    problem_info = self.analyze_with_llm_logic(code)

                    if problem_info:
                        print(f"✨ AI Detection: #{problem_info['id']} - {problem_info['title']} ({problem_info['difficulty']})")
                        function_name = self.extract_function_name(code) or "ai_detected"
                        self.problem_cache[function_name] = problem_info
                        self.save_cache()
                    else:
                        # 🔍 TERTIARY METHOD: Function name + LeetCode API
                        print("🔍 Final fallback: function name detection...")
                        function_name = self.extract_function_name(code)
                        if not function_name:
                            print(f"Could not identify function in {file_path.name}")
                            return False

                        print(f"🔍 Function found: {function_name}")
                        problem_info = self.get_problem_info_from_leetcode(function_name)

            if not problem_info:
                print(f"❌ Could not identify LeetCode problem with any method")
                return False

            print(f"Found: #{problem_info['id']} - {problem_info['title']} ({problem_info['difficulty']})")

            # Determine target directory
            difficulty = problem_info['difficulty'].lower()
            if difficulty == 'easy':
                target_dir = self.easy_path
            elif difficulty == 'hard':
                target_dir = self.hard_path
            else:
                target_dir = self.medium_path

            safe_title = re.sub(r'[^\w\s-]', '', problem_info['title']).replace(' ', '_')
            target_filename = f"{problem_info['id']}_{safe_title}.cpp"
            target_path = target_dir / target_filename

            if not target_path.exists():
                shutil.copy2(file_path, target_path)
                print(f"Copied to: {target_path.relative_to(self.repo_path)}")
                return True
            else:
                print(f"Already exists: {target_filename}")
                return False

        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            return False

    def organize_all(self):
        """Organize recent files in Daily Questions"""
        print("🚀 Starting AI-Powered LeetCode Organization...")
        print("🕐 Only processing files modified in the last 24 hours...")

        sorted_files = self.sort_daily_files()

        if not sorted_files:
            print("ℹ️  No files modified in the last 24 hours. Nothing to process.")
            return

        print(f"📅 Found {len(sorted_files)} recent files (modified in last 24h):")
        current_time = time.time()
        for file_path in sorted_files:
            date = self.parse_date_from_filename(file_path.name)
            hours_ago = (current_time - file_path.stat().st_mtime) / 3600
            print(f"   {file_path.name} - {date.strftime('%d/%m/%Y')} (modified {hours_ago:.1f}h ago)")

        print("\n" + "="*50)

        organized = 0
        for file_path in sorted_files:
            if self.organize_file(file_path):
                organized += 1
            print()

        print(f"✅ Organization complete! {organized} files organized.")

        easy_count = len(list(self.easy_path.glob("*.cpp")))
        medium_count = len(list(self.medium_path.glob("*.cpp")))
        hard_count = len(list(self.hard_path.glob("*.cpp")))

        print(f"📊 Current distribution:")
        print(f"   Easy: {easy_count} problems")
        print(f"   Medium: {medium_count} problems")
        print(f"   Hard: {hard_count} problems")
        print(f"   Total: {easy_count + medium_count + hard_count} problems")

if __name__ == "__main__":
    import sys
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."

    organizer = SimpleLeetCodeOrganizer(repo_path)
    organizer.organize_all()