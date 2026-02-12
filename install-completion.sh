#!/usr/bin/env bash
# Shell completion installer for qnote

set -e

PROG_NAME="qnote"

show_help() {
    cat << EOF
Usage: $0 [SHELL]

Install shell completion for qnote.

NOTE: If you installed qnote via .deb package, shell completion
is already installed system-wide. You don't need to run this script.
Just restart your shell!

This script is for users who installed via pip or from source.

Arguments:
  SHELL    Shell type: bash, zsh, or fish

Examples:
  $0 bash    Install bash completion
  $0 zsh     Install zsh completion
  $0 fish    Install fish completion

EOF
}

install_bash() {
    echo "Installing bash completion..."
    
    # Add to bashrc if not already present
    COMPLETION_LINE='eval "$(_QNOTE_COMPLETE=bash_source qnote)"'
    
    if ! grep -q "_QNOTE_COMPLETE" "$HOME/.bashrc" 2>/dev/null; then
        echo "" >> "$HOME/.bashrc"
        echo "# qnote completion" >> "$HOME/.bashrc"
        echo "$COMPLETION_LINE" >> "$HOME/.bashrc"
        echo "✓ Added completion to ~/.bashrc"
        echo "Run: source ~/.bashrc"
    else
        echo "✓ Completion already installed in ~/.bashrc"
    fi
}

install_zsh() {
    echo "Installing zsh completion..."
    
    # Add to zshrc if not already present
    COMPLETION_LINE='eval "$(_QNOTE_COMPLETE=zsh_source qnote)"'
    
    if ! grep -q "_QNOTE_COMPLETE" "$HOME/.zshrc" 2>/dev/null; then
        echo "" >> "$HOME/.zshrc"
        echo "# qnote completion" >> "$HOME/.zshrc"
        echo "$COMPLETION_LINE" >> "$HOME/.zshrc"
        echo "✓ Added completion to ~/.zshrc"
        echo "Run: source ~/.zshrc"
    else
        echo "✓ Completion already installed in ~/.zshrc"
    fi
}

install_fish() {
    echo "Installing fish completion..."
    
    # Create completions directory if it doesn't exist
    FISH_COMP_DIR="$HOME/.config/fish/completions"
    mkdir -p "$FISH_COMP_DIR"
    
    # Generate completion file
    _QNOTE_COMPLETE=fish_source qnote > "$FISH_COMP_DIR/qnote.fish"
    
    echo "✓ Created completion file at $FISH_COMP_DIR/qnote.fish"
    echo "Fish will load it automatically"
}

# Main script
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

SHELL_TYPE="$1"

case "$SHELL_TYPE" in
    bash)
        install_bash
        ;;
    zsh)
        install_zsh
        ;;
    fish)
        install_fish
        ;;
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        echo "Error: Unknown shell type: $SHELL_TYPE"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo "Shell completion installed successfully!"
