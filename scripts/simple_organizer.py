#!/usr/bin/env python3
"""
Simple LeetCode Repository Organizer
- Sorts Daily Questions by date
- Gets problem info from LeetCode API
- Organizes by difficulty with problem numbers
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

    def extract_function_name(self, code: str) -> Optional[str]:
        """Extract main function name from C++ code"""
        # Enhanced function detection - prioritize main solution functions

        # Priority 1: Look for non-static, non-helper functions in Solution class
        # These are typically the main LeetCode solution functions
        patterns = [
            # Pattern 1: Non-static public functions in Solution class (highest priority)
            r'class\s+Solution\s*{[^}]*public:\s*[^}]*?(?!static)(\w+)\s*\([^)]*\)\s*{',

            # Pattern 2: Any function that returns a common LeetCode type and has parameters
            r'((?:int|bool|string|vector|double|long|ListNode\*|TreeNode\*)\s+(\w+))\s*\([^)]+\)\s*{',

            # Pattern 3: Functions with typical LeetCode naming patterns
            r'(\w*(?:count|find|search|max|min|sum|calc|solve|get|is|can|has|check|valid|path|tree|list|array|sort|merge)\w*)\s*\([^)]*\)\s*{',
        ]

        all_functions = []

        for pattern in patterns:
            matches = re.findall(pattern, code, re.DOTALL | re.IGNORECASE)
            if matches:
                # Enhanced filtering
                exclude = {
                    'Solution', 'main', 'int', 'bool', 'string', 'vector', 
                    'if', 'for', 'while', 'do', 'switch', 'case', 'return',
                    'comp', 'compare', 'cmp', 'sort', 'less', 'greater',  # Common helper function names
                    'helper', 'util', 'dfs', 'bfs', 'backtrack'  # Common helper patterns
                }

                for match in matches:
                    # Handle tuple matches from pattern 2
                    if isinstance(match, tuple):
                        function_name = match[1] if len(match) > 1 else match[0]
                    else:
                        function_name = match

                    if (function_name and 
                        function_name.lower() not in exclude and 
                        len(function_name) > 2 and
                        not function_name.startswith('_') and  # Avoid private functions
                        function_name[0].islower()):  # LeetCode functions start with lowercase

                        all_functions.append(function_name)

        if all_functions:
            # Remove duplicates while preserving order
            unique_functions = list(dict.fromkeys(all_functions))

            # Prefer longer, more descriptive function names (likely main functions)
            # Sort by length descending, then alphabetically
            best_function = max(unique_functions, key=lambda f: (len(f), f.lower()))

            return best_function

        return None

    def get_problem_info_from_leetcode(self, function_name: str) -> Optional[Dict]:
        """Get problem info from LeetCode GraphQL API"""
        if function_name in self.problem_cache:
            return self.problem_cache[function_name]

        try:
            # LeetCode GraphQL endpoint
            url = "https://leetcode.com/graphql"

            # Query to search for problems by title slug
            query = """
            query questionData($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionId
                    questionFrontendId
                    title
                    difficulty
                    topicTags {
                        name
                    }
                }
            }
            """

            # Try different variations of function name as title slug
            variations = [
                function_name.lower(),
                re.sub(r'([A-Z])', r'-\1', function_name).lower().strip('-'),
                function_name.lower().replace('_', '-')
            ]

            for variation in variations:
                payload = {
                    "query": query,
                    "variables": {"titleSlug"
                                  : variation}
                }

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
        """Sort daily files by date and filter by recent files (last 24 hours)"""
        files = list(self.daily_path.glob("*.cpp"))

        # Filter files modified in the last 24 hours
        recent_files = []
        current_time = time.time()
        one_day_ago = current_time - (24 * 60 * 60)  # 24 hours in seconds

        for file_path in files:
            # Check file modification time
            file_mtime = file_path.stat().st_mtime
            if file_mtime >= one_day_ago:
                recent_files.append(file_path)

        if recent_files:
            return sorted(recent_files, key=lambda f: self.parse_date_from_filename(f.name))
        else:
            # If no recent files, return empty list instead of all files
            return []

    def organize_file(self, file_path: Path) -> bool:
        """Organize a single file"""
        try:
            print(f"Processing: {file_path.name}")

            # Read code
            with open(file_path, 'r') as f:
                code = f.read()

            # Extract function name
            function_name = self.extract_function_name(code)
            if not function_name:
                print(f"Could not identify function in {file_path.name}")
                return False

            print(f"🔍 Function found: {function_name}")

            # Get problem info from LeetCode
            problem_info = self.get_problem_info_from_leetcode(function_name)
            if not problem_info:
                print(f"Could not find LeetCode problem for {function_name}")
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

            # Create target filename: "1_Two_Sum.cpp"
            safe_title = re.sub(r'[^\w\s-]', '', problem_info['title']).replace(' ', '_')
            target_filename = f"{problem_info['id']}_{safe_title}.cpp"
            target_path = target_dir / target_filename

            # Copy file
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
        """Organize all files in Daily Questions"""
        print("🚀 Starting Simple LeetCode Organization...")
        print("🕐 Only processing files modified in the last 24 hours...")

        # Get recent files sorted by date
        sorted_files = self.sort_daily_files()

        if not sorted_files:
            print("ℹ️  No files modified in the last 24 hours. Nothing to process.")
            print("🎯 This prevents unnecessary API calls for already processed files.")
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
            print()  # Empty line between files

        print(f"✅ Organization complete! {organized} files organized.")

        # Show summary
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