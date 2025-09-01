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
        # Look for main function in Solution class
        patterns = [
            r'class\s+Solution\s*{[^}]*public:[^}]*?(\w+)\s*\([^)]*\)\s*{',
            r'(\w+)\s*\([^)]*\)\s*{[^}]*return',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, code, re.DOTALL | re.IGNORECASE)
            if matches:
                # Filter out common non-function words
                exclude = {'Solution', 'main', 'int', 'bool', 'string', 'vector', 'if', 'for', 'while'}
                for match in matches:
                    if match and match not in exclude and len(match) > 2:
                        return match
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
        """Sort daily files by date"""
        files = list(self.daily_path.glob("*.cpp"))
        return sorted(files, key=lambda f: self.parse_date_from_filename(f.name))

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

        # Get sorted files by date
        sorted_files = self.sort_daily_files()

        print(f"📅 Found {len(sorted_files)} daily files (sorted by date):")
        for file_path in sorted_files:
            date = self.parse_date_from_filename(file_path.name)
            print(f"   {file_path.name} - {date.strftime('%d/%m/%Y')}")

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