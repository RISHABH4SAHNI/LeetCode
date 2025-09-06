# LeetCode Daily Solutions

This repository contains my daily practice solutions to [LeetCode](https://leetcode.com/u/f20211630/) problems.  

---

## Structure
- `Easy/` → Easy-level problems (organized copies)
- `Medium/` → Medium-level problems (organized copies)  
- `Hard/` → Hard-level problems (organized copies)
- `Daily Questions/` → Your original solution files (kept with original names)

---

## Automated Organization 🤖

This repository uses **automated organization**! Here's how it works:

### How to Add New Solutions
1. **Add your solution file** to the `Daily Questions/` folder with any filename (e.g., `07:09:2025.cpp`)
2. **Push to GitHub** - that's it! 

### What Happens Automatically
- 🔍 **Auto-detection**: The system analyzes your code and git commit messages to identify the LeetCode problem
- � **Dual storage**: Your original file stays in `Daily Questions/` with its original name
- �📁 **Auto-organization**: A copy is created in the correct difficulty folder (`Easy/`, `Medium/`, `Hard/`)
- 🏷️ **Auto-naming**: The copy is renamed to format: `{problem_number}_{problem_title}.cpp`
- 🧹 **Duplicate cleanup**: Automatically removes any duplicate files in difficulty folders

### Triggers
- ✅ **GitHub Actions**: Triggers automatically when you push files to `Daily Questions/` folder
- ✅ **Pre-push Hook**: Local organization before pushing (optional)

### Manual Organization
You can also run the organizer manually:
```bash
# Organize recent files (last 24 hours)
./leetcode_env/bin/python scripts/simple_organizer.py

# Organize all files in Daily Questions folder
./leetcode_env/bin/python scripts/simple_organizer.py --auto-mode

# Test the workflow
./scripts/test_workflow.sh
```

---

## My LeetCode Profile
[LeetCode Profile](https://leetcode.com/u/f20211630/)

---

Consistency over time is the key to mastering problem-solving.
