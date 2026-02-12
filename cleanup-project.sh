#!/bin/bash
# Cleanup script for qnote project
# Removes build artifacts, temporary files, and unnecessary files

set -e

echo "======================================"
echo "qnote Project Cleanup"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "setup.py" ] || [ ! -d "qnote" ]; then
    echo -e "${RED}Error: This doesn't look like the qnote project directory${NC}"
    echo "Please run this script from the qnote project root"
    exit 1
fi

echo -e "${YELLOW}Cleaning up project...${NC}"
echo ""

# Function to remove if exists
remove_if_exists() {
    if [ -e "$1" ]; then
        rm -rf "$1"
        echo -e "${GREEN}✓${NC} Removed: $1"
    fi
}

# Python build artifacts
echo "Removing Python build artifacts..."
remove_if_exists "build/"
remove_if_exists "dist/"
remove_if_exists ".pybuild/"
remove_if_exists "*.egg-info"
remove_if_exists "qnote.egg-info/"
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type f -name "*~" -delete 2>/dev/null || true

# Debian build artifacts
echo ""
echo "Removing Debian build artifacts..."
remove_if_exists "debian/.debhelper/"
remove_if_exists "debian/qnote/"
remove_if_exists "debian/files"
remove_if_exists "debian/*.debhelper*"
remove_if_exists "debian/*.substvars"
remove_if_exists "debian/*.log"
remove_if_exists "debian-package/"

# Remove built .deb files from parent directory
echo ""
echo "Removing .deb packages..."
remove_if_exists "../qnote_*.deb"
remove_if_exists "../qnote_*.buildinfo"
remove_if_exists "../qnote_*.changes"
remove_if_exists "../qnote_*.dsc"
remove_if_exists "../qnote_*.tar.*"

# RPM build artifacts (if any)
remove_if_exists "qnote.spec"

# Test artifacts
echo ""
echo "Removing test artifacts..."
remove_if_exists ".pytest_cache/"
remove_if_exists ".coverage"
remove_if_exists "htmlcov/"
remove_if_exists ".tox/"
remove_if_exists ".mypy_cache/"

# Database files (test databases)
echo ""
echo "Removing test database files..."
find . -name "*.db" -not -path "./docs/*" -delete 2>/dev/null || true
find . -name "test_*.db" -delete 2>/dev/null || true

# Editor backup files
echo ""
echo "Removing editor backup files..."
find . -name "*.swp" -delete 2>/dev/null || true
find . -name "*.swo" -delete 2>/dev/null || true
find . -name ".*.swp" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true

# IDE files (optional - uncomment if you want to remove)
# remove_if_exists ".vscode/"
# remove_if_exists ".idea/"

# Virtual environment (optional - uncomment if you want to remove)
# remove_if_exists "venv/"
# remove_if_exists "env/"
# remove_if_exists ".venv/"

# Temporary files
echo ""
echo "Removing temporary files..."
remove_if_exists "fix.sh"
remove_if_exists "add-debian-packaging.sh"
remove_if_exists ".DS_Store"
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true

# Optional: Remove old project files
echo ""
echo "Removing old project files..."
remove_if_exists "../qnote-project.zip"
remove_if_exists "../quick-note-projektplan.md"
remove_if_exists "../znuny-todos-qnote.md"

echo ""
echo -e "${GREEN}======================================"
echo "Cleanup Complete! ✨"
echo "======================================${NC}"
echo ""
echo "Your project is now clean and ready for:"
echo "  - Building: ./build-deb.sh"
echo "  - Development: pip install -e ."
echo "  - Git commit: git add . && git commit"
echo ""

# Show remaining size
if command -v du &> /dev/null; then
    SIZE=$(du -sh . | cut -f1)
    echo "Project size: $SIZE"
    echo ""
fi
