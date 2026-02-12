# Shell Completion

This document explains how to enable tab completion for qnote in various shells.

## Overview

qnote supports command and option completion for:
- Bash
- Zsh  
- Fish

Tab completion helps you:
- Complete commands and subcommands
- Show available options
- Complete file paths
- Complete tag names (future)

## Automatic Installation (.deb Package)

**If you installed qnote via .deb package, shell completion is already installed!**

The .deb package automatically installs completion files to:
- Bash: `/etc/bash_completion.d/qnote`
- Zsh: `/usr/share/zsh/vendor-completions/_qnote`
- Fish: `/usr/share/fish/vendor_completions.d/qnote.fish`

**After installing the .deb package:**

### Bash
```bash
# Restart your shell or reload bashrc
exec bash
# OR
source ~/.bashrc
```

### Zsh
```bash
# Restart your shell or reload zshrc
exec zsh
# OR
source ~/.zshrc
```

### Fish
```bash
# Fish reloads completions automatically
# Just start a new terminal or run:
exec fish
```

## Manual Installation (pip/source installation)

If you installed via pip or from source, use these methods:

### Bash

Add to `~/.bashrc`:

```bash
# qnote completion
eval "$(_QNOTE_COMPLETE=bash_source qnote)"
```

Then reload:

```bash
source ~/.bashrc
```

### Zsh

Add to `~/.zshrc`:

```bash
# qnote completion
eval "$(_QNOTE_COMPLETE=zsh_source qnote)"
```

Then reload:

```bash
source ~/.zshrc
```

### Fish

One-time setup:

```bash
# Create completion file
_QNOTE_COMPLETE=fish_source qnote > ~/.config/fish/completions/qnote.fish
```

Fish loads completions automatically.

## Usage Examples

### Basic Completion

```bash
# Complete commands
qnote <TAB>
# Shows: add, list, show, edit, delete, search, snippet, todo, config, sync

# Complete subcommands
qnote snippet <TAB>
# Shows: add, list, show, edit, delete

# Complete todo subcommands
qnote todo <TAB>
# Shows: add, list, show, done, undone, edit, delete
```

### Config Command Completion (NEW!)

The config commands have intelligent completion:

```bash
# Complete config subcommands
qnote config <TAB>
# Shows: list, get, set, reset, path

# Complete config keys with descriptions
qnote config set <TAB>
# Shows:
#   editor          Text editor command (vim, nvim, nano, code, etc.)
#   theme           Color theme (auto, dark, light)
#   pager           Pager command (less, more, cat)
#   database.path   SQLite database file path
#   sync.remote     Git remote URL for sync
#   sync.auto       Enable automatic sync (true/false)

# Complete config values based on key
qnote config set editor <TAB>
# Shows: vim, nvim, nano, emacs, code, vi

qnote config set theme <TAB>
# Shows: auto, dark, light

qnote config set sync.auto <TAB>
# Shows: true, false

# Same for config get
qnote config get <TAB>
# Shows all available config keys with descriptions
```

### Language Completion for Snippets

```bash
# Complete programming languages
qnote snippet add "code" -l <TAB>
# Shows: python, bash, javascript, typescript, java, c, cpp, rust, go, ruby, php, etc.

qnote snippet list --language <TAB>
# Shows: python, bash, javascript, typescript, java, c, cpp, rust, go, ruby, php, etc.
```

### Option Completion

```bash
# Show options for add command
qnote add --<TAB>
# Shows: --tags, --editor, --title, --starred

# Complete priority values
qnote todo add "task" --priority <TAB>
# Shows: low, medium, high

# Complete sort options
qnote list --sort <TAB>
# Shows: created, updated, title
```

### File Path Completion

```bash
# Complete file paths
qnote snippet add --from-file <TAB>
# Shows: available files in current directory
```

## Advanced Configuration

### Bash - Lazy Loading

For faster shell startup, use lazy loading:

```bash
# In ~/.bashrc
_qnote_completion() {
    eval "$(_QNOTE_COMPLETE=bash_source qnote)"
}

# Load on first use
alias qnote='_qnote_completion; unset -f _qnote_completion; qnote'
```

### Zsh - Completion Cache

Enable completion caching:

```zsh
# In ~/.zshrc
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path ~/.zsh/cache

# Then add qnote completion
eval "$(_QNOTE_COMPLETE=zsh_source qnote)"
```

### Fish - Custom Completions

Create custom completions in `~/.config/fish/completions/qnote.fish`:

```fish
# Generated completions
_QNOTE_COMPLETE=fish_source qnote > ~/.config/fish/completions/qnote.fish

# Add custom completions
complete -c qnote -n '__fish_use_subcommand' -a 'add' -d 'Add a new note'
complete -c qnote -n '__fish_use_subcommand' -a 'list' -d 'List all notes'
```

## Troubleshooting

### Completion Not Working

**Bash:**
```bash
# Check if completion is loaded
complete -p qnote

# Reload bashrc
source ~/.bashrc

# Install bash-completion package
sudo apt install bash-completion  # Debian/Ubuntu
sudo dnf install bash-completion  # Fedora
```

**Zsh:**
```bash
# Enable completion system
autoload -Uz compinit && compinit

# Reload zshrc
source ~/.zshrc

# Check if loaded
which _qnote
```

**Fish:**
```bash
# Check completion file exists
ls ~/.config/fish/completions/qnote.fish

# Regenerate if needed
_QNOTE_COMPLETE=fish_source qnote > ~/.config/fish/completions/qnote.fish

# Reload completions
fish_update_completions
```

### Slow Completion

**Bash:**
```bash
# Disable programmable completion temporarily
shopt -u progcomp

# Check which completions are slow
time complete -p

# Use lazy loading (see Advanced Configuration above)
```

**Zsh:**
```zsh
# Enable completion cache (see Advanced Configuration above)
zstyle ':completion:*' use-cache on
```

### Completion Cache Issues

**Bash:**
```bash
# Clear completion cache
hash -r
```

**Zsh:**
```zsh
# Rebuild completion cache
rm -f ~/.zcompdump
compinit
```

**Fish:**
```bash
# Clear fish completions
rm -rf ~/.cache/fish/
```

## Completion Features

### Currently Supported

- Command names (add, list, show, etc.)
- Subcommand names (snippet add, todo list, etc.)
- Option names (--tags, --editor, etc.)
- Choice values (--priority low|medium|high)
- File paths (--from-file)

### Future Enhancements

- Tag name completion from database
- Note ID completion with titles
- Language name completion for snippets
- Date completion for TODOs
- Custom completion scripts

## Implementation Details

qnote uses Click's built-in completion support:

```python
# In cli.py
import click

@click.group()
def main():
    """qnote - Quick Note Manager"""
    pass

# Completion is automatically generated
```

To add completion to custom commands:

```python
@click.command()
@click.option('--language', type=click.Choice(['python', 'bash', 'rust']))
def snippet_add(language):
    """Add a snippet"""
    pass
```

## Testing Completion

### Test Bash Completion

```bash
# Get completion script
_QNOTE_COMPLETE=bash_source qnote

# Test specific completion
_QNOTE_COMPLETE=bash_complete qnote snippet
```

### Test Zsh Completion

```zsh
# Get completion script  
_QNOTE_COMPLETE=zsh_source qnote

# Test specific completion
_QNOTE_COMPLETE=zsh_complete qnote todo
```

### Test Fish Completion

```fish
# Generate completion
_QNOTE_COMPLETE=fish_source qnote

# Test interactively
qnote <TAB>
```

## See Also

- [INSTALL.md](INSTALL.md) - Installation guide
- [USAGE.md](USAGE.md) - Command reference
- [CONFIG.md](CONFIG.md) - Configuration guide
- bash-completion(7) - Bash completion manual
- zshcompsys(1) - Zsh completion system
