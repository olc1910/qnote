# Tab Completion Testing Guide

## What Should Work

### Basic Command Completion

```bash
qnote <TAB>
# Shows: add, list, show, edit, delete, search, snippet, todo, config, sync
```

### Subcommand Completion

```bash
qnote snippet <TAB>
# Shows: add, list, show, edit, delete

qnote todo <TAB>
# Shows: add, list, show, done, undone, edit, delete

qnote config <TAB>
# Shows: list, get, set, reset, path
```

### Config Set - Key Completion (MOST IMPORTANT!)

```bash
qnote config set <TAB>
# Shows:
#   editor          Text editor command (vim, nvim, nano, code, etc.)
#   theme           Color theme (auto, dark, light)
#   pager           Pager command (less, more, cat)
#   database.path   SQLite database file path
#   sync.remote     Git remote URL for sync
#   sync.auto       Enable automatic sync (true/false)
```

### Config Set - Value Completion

```bash
qnote config set editor <TAB>
# Shows: vim, nvim, nano, emacs, code, vi

qnote config set theme <TAB>
# Shows: auto, dark, light

qnote config set sync.auto <TAB>
# Shows: true, false
```

### Config Get - Key Completion

```bash
qnote config get <TAB>
# Shows same keys as config set
```

### Language Completion for Snippets

```bash
qnote snippet add "code" -l <TAB>
# Shows: python, bash, javascript, typescript, java, c, cpp, rust, go, etc.

qnote snippet list --language <TAB>
# Shows: python, bash, javascript, typescript, java, c, cpp, rust, go, etc.
```

### Option Completion

```bash
qnote list --<TAB>
# Shows: --tags, --limit, --sort, --starred, --help

qnote list --sort <TAB>
# Shows: created, updated, title

qnote todo add "task" --priority <TAB>
# Shows: low, medium, high
```

## Testing After .deb Installation

### 1. Install Package

```bash
./build-deb.sh
sudo dpkg -i ../qnote_0.1.0-1_all.deb
```

### 2. Restart Shell

**CRITICAL:** Must restart shell for completion to work!

```bash
exec bash   # For bash
exec zsh    # For zsh
exec fish   # For fish
```

### 3. Test Basic Completion

```bash
qnote <TAB><TAB>
```

You should see all commands. If not, check:

```bash
# Bash - check if file exists
ls -la /etc/bash_completion.d/qnote
cat /etc/bash_completion.d/qnote

# Check if completion is loaded
complete -p qnote
```

### 4. Test Config Completion (Most Important!)

```bash
qnote config set <TAB><TAB>
```

Should show:
```
editor          theme           pager
database.path   sync.remote     sync.auto
```

If you see descriptions, even better!

Then test value completion:

```bash
qnote config set theme <TAB><TAB>
```

Should show:
```
auto  dark  light
```

### 5. Test Language Completion

```bash
qnote snippet add "test" -l <TAB><TAB>
```

Should show common languages.

## Troubleshooting

### Completion Not Working at All

```bash
# 1. Check if completion file exists
ls /etc/bash_completion.d/qnote

# 2. Check if it's executable (should be readable, not executable)
cat /etc/bash_completion.d/qnote

# 3. Manually source it
source /etc/bash_completion.d/qnote

# 4. Check if complete command is registered
complete -p qnote

# 5. Test Click's completion directly
_QNOTE_COMPLETE=bash_complete qnote

# 6. Restart shell again
exec bash
```

### Config Keys Not Showing Descriptions

This depends on your bash-completion version. The completions will work, but descriptions might not show. That's OK - the keys will still complete.

### Only First Level Completes

If `qnote <TAB>` works but `qnote config <TAB>` doesn't:

```bash
# Update bash-completion
sudo apt update
sudo apt install --reinstall bash-completion

# Restart shell
exec bash
```

### Fish/Zsh Not Working

```bash
# Fish - check file
ls /usr/share/fish/vendor_completions.d/qnote.fish

# Fish - reload
fish_update_completions

# Zsh - check file
ls /usr/share/zsh/vendor-completions/_qnote

# Zsh - rebuild cache
rm -f ~/.zcompdump*
compinit
```

## Manual Testing Script

Save as `test-completion.sh`:

```bash
#!/bin/bash
echo "=== Testing qnote completion ==="
echo ""

echo "1. Testing basic command completion:"
echo "   qnote <TAB> should show: add, list, show, etc."
echo ""

echo "2. Testing config subcommands:"
echo "   qnote config <TAB> should show: list, get, set, reset, path"
echo ""

echo "3. Testing config set keys:"
echo "   qnote config set <TAB> should show:"
echo "     - editor"
echo "     - theme"
echo "     - pager"
echo "     - database.path"
echo "     - sync.remote"
echo "     - sync.auto"
echo ""

echo "4. Testing config set values:"
echo "   qnote config set theme <TAB> should show: auto, dark, light"
echo ""

echo "5. Testing snippet language completion:"
echo "   qnote snippet add 'code' -l <TAB> should show: python, bash, etc."
echo ""

echo "Now test manually with TAB key!"
echo ""
echo "Check completion is loaded:"
complete -p qnote
```

## Expected Behavior Summary

✅ **Working:**
- Basic commands: `qnote <TAB>`
- Subcommands: `qnote config <TAB>`, `qnote snippet <TAB>`
- Config keys: `qnote config set <TAB>` with descriptions
- Config values: `qnote config set theme <TAB>`
- Languages: `qnote snippet add -l <TAB>`
- Options: `qnote list --sort <TAB>`
- Priorities: `qnote todo add -p <TAB>`

✅ **After .deb install:**
- No manual setup needed
- Just restart shell
- Works immediately

✅ **Completion features:**
- Shows all available options
- Shows descriptions for config keys
- Shows valid values for known keys
- Filters as you type
