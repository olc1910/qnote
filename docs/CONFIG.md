# Configuration Reference

This document describes qnote's configuration system.

## Configuration File

Location: `~/.config/qnote/config.yaml`

The configuration file is created automatically on first run with default values.

## Configuration Format

qnote uses YAML format for configuration.

### Default Configuration

```yaml
# Editor for writing notes and snippets
editor: vim

# Color theme: auto, dark, or light
theme: auto

# Pager for viewing long output
pager: less

# Synchronization settings (not implemented)
sync:
  remote: null
  auto: false

# Database location
database:
  path: ~/.local/share/qnote/qnote.db
```

## Configuration Options

### editor

Default editor for writing notes and editing content.

**Type:** string  
**Default:** vim  
**Valid values:** vim, nvim, nano, emacs, code, any editor command

**Examples:**
```yaml
editor: nvim
editor: nano
editor: code --wait
editor: emacs -nw
```

**Environment override:**
```bash
export EDITOR=nvim
```

### theme

Terminal color theme.

**Type:** string  
**Default:** auto  
**Valid values:** auto, dark, light

**Examples:**
```yaml
theme: dark   # Force dark theme
theme: light  # Force light theme
theme: auto   # Auto-detect from terminal
```

### pager

Pager for viewing long output.

**Type:** string  
**Default:** less  
**Valid values:** less, more, cat, any pager command

**Examples:**
```yaml
pager: less -R
pager: more
pager: cat
```

### database.path

Location of SQLite database file.

**Type:** string  
**Default:** ~/.local/share/qnote/qnote.db

**Examples:**
```yaml
database:
  path: ~/Dropbox/qnote/qnote.db
  path: /var/lib/qnote/notes.db
```

**Environment override:**
```bash
export QNOTE_DB=/path/to/database.db
```

### sync.remote

Remote Git repository URL for synchronization.

**Type:** string or null  
**Default:** null  
**Status:** Not implemented

**Examples:**
```yaml
sync:
  remote: git@github.com:user/notes.git
  remote: https://github.com/user/qnote-sync.git
```

### sync.auto

Enable automatic synchronization.

**Type:** boolean  
**Default:** false  
**Status:** Not implemented

**Examples:**
```yaml
sync:
  auto: true
  auto: false
```

## Environment Variables

Environment variables override configuration file settings.

### EDITOR

Preferred text editor.

```bash
export EDITOR=nvim
```

Overrides `editor` in config file.

### QNOTE_DB

Database file location.

```bash
export QNOTE_DB=/path/to/custom.db
```

Overrides `database.path` in config file.

### QNOTE_CONFIG

Configuration file location.

```bash
export QNOTE_CONFIG=/path/to/custom/config.yaml
```

Uses custom config file instead of default.

### PAGER

Output pager.

```bash
export PAGER="less -R"
```

Overrides `pager` in config file.

## Managing Configuration

### View Configuration

```bash
qnote config list
```

### Set Values

```bash
# Set editor
qnote config set editor nvim

# Set theme
qnote config set theme dark

# Set database path
qnote config set database.path ~/notes.db
```

### Edit Manually

```bash
# Open config file in editor
$EDITOR ~/.config/qnote/config.yaml

# Or use qnote itself
vim ~/.config/qnote/config.yaml
```

### Reset to Defaults

```bash
# Remove config file
rm ~/.config/qnote/config.yaml

# Run qnote to recreate defaults
qnote add "test"
```

## Configuration Examples

### Minimal Configuration

```yaml
editor: vim
theme: auto
```

### Complete Configuration

```yaml
# Editor configuration
editor: nvim

# Visual settings
theme: dark
pager: less -R

# Database location
database:
  path: ~/Dropbox/qnote/qnote.db

# Sync settings (future)
sync:
  remote: git@github.com:user/notes.git
  auto: false
```

### VS Code Integration

```yaml
editor: code --wait
theme: light
```

### Dropbox Sync

```yaml
database:
  path: ~/Dropbox/qnote/notes.db
```

### Network Storage

```yaml
database:
  path: /mnt/nas/qnote/notes.db
```

## Troubleshooting

### Config File Not Found

qnote creates the config file automatically:

```bash
# Force config creation
qnote add "test"

# Check location
ls -la ~/.config/qnote/config.yaml
```

### Invalid YAML Syntax

Validate YAML syntax:

```bash
# Install yamllint
pip install yamllint

# Check config file
yamllint ~/.config/qnote/config.yaml
```

### Editor Not Working

Check editor command:

```bash
# Test editor command
vim --version

# Set in environment
export EDITOR=nvim
```

### Database Permission Errors

Fix permissions:

```bash
# Check permissions
ls -l ~/.local/share/qnote/

# Fix ownership
chown -R $USER ~/.local/share/qnote/
```

## Configuration Priority

Settings are applied in this order (later overrides earlier):

1. Default values (hardcoded)
2. Configuration file (`~/.config/qnote/config.yaml`)
3. Environment variables (`EDITOR`, `QNOTE_DB`, etc.)
4. Command-line flags (where applicable)

## See Also

- [INSTALL.md](INSTALL.md) - Installation guide
- [USAGE.md](USAGE.md) - Command reference
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
