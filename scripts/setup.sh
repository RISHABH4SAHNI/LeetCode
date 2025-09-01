#!/bin/bash

# Setup Simple LeetCode Organizer

echo "🚀 Setting up Simple LeetCode Organizer..."

# Install Python requests if needed
pip3 install --user requests 2>/dev/null || echo "✅ Python requests already installed"

# Make scripts executable
chmod +x scripts/simple_organizer.py
chmod +x scripts/organize.sh

# Create git alias
git config alias.organize '!bash scripts/organize.sh'

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Usage:"
echo "  git organize                     → Organize all files"
echo "  python3 scripts/simple_organizer.py  → Run organizer manually"
echo ""
echo "🎯 Just add your .cpp files to 'Daily Questions/' folder"
echo "   The organizer will handle the rest!"