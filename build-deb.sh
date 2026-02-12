#!/bin/bash
# Build .deb package for qnote

set -e  # Exit on error

echo "======================================"
echo "Building qnote Debian Package"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if required tools are installed
check_requirements() {
    echo -e "${YELLOW}Checking requirements...${NC}"
    
    local missing=""
    
    if ! command -v dpkg-buildpackage &> /dev/null; then
        missing="${missing}devscripts "
    fi
    
    if ! command -v dh &> /dev/null; then
        missing="${missing}debhelper "
    fi
    
    if ! command -v python3 &> /dev/null; then
        missing="${missing}python3 "
    fi
    
    if [ -n "$missing" ]; then
        echo -e "${RED}Error: Missing required packages: ${missing}${NC}"
        echo ""
        echo "Install with:"
        echo "  sudo apt install debhelper devscripts dh-python python3-all python3-setuptools"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All requirements satisfied${NC}"
    echo ""
}

# Clean previous builds
clean_build() {
    echo -e "${YELLOW}Cleaning previous builds...${NC}"
    
    if [ -f debian/rules ]; then
        fakeroot debian/rules clean 2>/dev/null || true
    fi
    
    rm -rf debian/.debhelper/ debian/qnote/ debian/files
    rm -rf debian/*.debhelper* debian/*.substvars
    rm -f ../qnote_*.deb ../qnote_*.build* ../qnote_*.changes
    
    echo -e "${GREEN}✓ Cleaned${NC}"
    echo ""
}

# Build the package
build_package() {
    echo -e "${YELLOW}Building package...${NC}"
    echo ""
    
    # Build binary package only (-b), unsigned (-us -uc)
    dpkg-buildpackage -us -uc -b
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Package built successfully!${NC}"
    else
        echo ""
        echo -e "${RED}✗ Build failed!${NC}"
        exit 1
    fi
}

# Show results
show_results() {
    echo ""
    echo "======================================"
    echo "Build Results"
    echo "======================================"
    echo ""
    
    # Find the .deb file
    DEB_FILE=$(ls -t ../*.deb 2>/dev/null | head -1)
    
    if [ -n "$DEB_FILE" ]; then
        echo -e "${GREEN}Package created:${NC}"
        echo "  $DEB_FILE"
        echo ""
        
        # Show package info
        echo "Package information:"
        dpkg-deb --info "$DEB_FILE" | grep -E "Package:|Version:|Architecture:|Description:" || true
        echo ""
        
        # Show file size
        SIZE=$(du -h "$DEB_FILE" | cut -f1)
        echo "Size: $SIZE"
        echo ""
        
        echo -e "${GREEN}Installation instructions:${NC}"
        echo "  sudo dpkg -i $DEB_FILE"
        echo "  sudo apt-get install -f  # Fix any missing dependencies"
        echo ""
        
        echo -e "${GREEN}Test installation:${NC}"
        echo "  qnote --version"
        echo "  qnote --help"
        echo ""
        
        echo -e "${GREEN}Uninstall:${NC}"
        echo "  sudo apt remove qnote"
        echo ""
    else
        echo -e "${RED}No .deb file found!${NC}"
        exit 1
    fi
}

# Main execution
main() {
    # Check we're in the right directory
    if [ ! -f "setup.py" ] || [ ! -d "qnote" ]; then
        echo -e "${RED}Error: Must be run from qnote project root directory${NC}"
        echo "Expected structure:"
        echo "  qnote-complete/"
        echo "  ├── qnote/"
        echo "  ├── debian/"
        echo "  └── setup.py"
        exit 1
    fi
    
    check_requirements
    clean_build
    build_package
    show_results
    
    echo -e "${GREEN}======================================"
    echo "Build Complete! 🎉"
    echo "======================================${NC}"
}

# Run main function
main "$@"
