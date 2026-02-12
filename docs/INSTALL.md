# Installation Guide

This document describes how to install qnote on your system.

## Requirements

- Python 3.8 or later
- pip (Python package manager)
- SQLite3 (usually pre-installed on Linux)

## Installation Methods

### 1. From .deb Package (Debian/Ubuntu)

Recommended for Debian-based distributions.

```bash
# Build the package
./build-deb.sh

# Install
sudo dpkg -i ../qnote_0.1.0-1_all.deb

# Fix any missing dependencies
sudo apt-get install -f
```

### 2. From Source with pip

Works on any Linux distribution.

```bash
# Install for current user
pip install --user -e .

# Or install system-wide (requires sudo)
sudo pip install -e .
```

### 3. Development Installation

For contributing or testing.

```bash
# Clone repository
git clone https://github.com/olc1910/qnote
cd qnote

# Install with development dependencies
pip install --user -e ".[dev]"

# Verify installation
qnote --version
```

## Shell Completion

Enable tab completion for your shell:

```bash
# Bash (add to ~/.bashrc)
eval "$(qnote --completion bash)"

# Zsh (add to ~/.zshrc)
eval "$(qnote --completion zsh)"

# Fish (one-time setup)
qnote --completion fish > ~/.config/fish/completions/qnote.fish
```

See [COMPLETION.md](COMPLETION.md) for details.

## Post-Installation

### Verify Installation

```bash
# Check version
qnote --version

# View help
qnote --help

# Create first note
qnote add "Installation complete"
```

### Configuration

qnote creates its configuration file on first run:

```
~/.config/qnote/config.yaml
```

See [CONFIG.md](CONFIG.md) for configuration options.

### Database Location

The SQLite database is stored at:

```
~/.local/share/qnote/qnote.db
```

Override with environment variable:

```bash
export QNOTE_DB=/path/to/custom/location.db
```

## Build Dependencies

For building .deb packages:

```bash
sudo apt install debhelper dh-python python3-all python3-setuptools devscripts
```

## Uninstallation

### Remove .deb Package

```bash
sudo dpkg -r qnote
```

### Remove pip Installation

```bash
pip uninstall qnote
```

### Remove User Data

```bash
# Remove configuration and database
rm -rf ~/.config/qnote ~/.local/share/qnote
```

## Troubleshooting

### Command not found

If `qnote` command is not found after pip installation:

```bash
# Add user bin to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell configuration
source ~/.bashrc  # or source ~/.zshrc
```

### Permission Denied

If you get permission errors:

```bash
# Use --user flag with pip
pip install --user -e .

# Or fix permissions
chmod +x ~/.local/bin/qnote
```

### Missing Dependencies

After .deb installation:

```bash
sudo apt-get install -f
```

For pip installation:

```bash
pip install --user click rich pygments pyyaml
```

### Database Errors

Reset the database:

```bash
# Backup existing data
cp ~/.local/share/qnote/qnote.db ~/.local/share/qnote/qnote.db.backup

# Remove and recreate
rm ~/.local/share/qnote/qnote.db
qnote add "test"  # Recreates database
```

## Platform-Specific Notes

### Arch Linux

```bash
# Install dependencies
sudo pacman -S python python-pip

# Install qnote
pip install --user -e .
```

### Fedora/RHEL

```bash
# Install dependencies
sudo dnf install python3 python3-pip

# Install qnote
pip install --user -e .
```

### macOS

```bash
# Install dependencies via Homebrew
brew install python

# Install qnote
pip3 install --user -e .
```

## See Also

- [USAGE.md](USAGE.md) - Command reference
- [CONFIG.md](CONFIG.md) - Configuration guide
- [PACKAGING.md](PACKAGING.md) - Package building
