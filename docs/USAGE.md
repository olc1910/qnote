# Command Reference

Complete reference for all qnote commands.

## Synopsis

```
qnote [OPTIONS] COMMAND [ARGS]...
```

## Global Options

```
--version              Show version and exit
--help                 Show help message
```

## Commands Overview

| Command | Description |
|---------|-------------|
| add | Create a new note |
| list | List all notes |
| show | Display a specific note |
| edit | Edit an existing note |
| delete | Delete note(s) |
| search | Search notes, snippets, and TODOs |
| snippet | Manage code snippets |
| todo | Manage TODO items |
| config | Manage configuration |
| sync | Synchronize notes (not implemented) |

---

## Note Commands

### qnote add

Create a new note.

**Usage:**
```bash
qnote add [OPTIONS] [CONTENT]
```

**Options:**
```
-t, --tags TEXT        Comma-separated tags
-e, --editor           Open external editor
--title TEXT           Note title
--starred              Mark as starred/favorite
```

**Examples:**
```bash
# Quick note
qnote add "Remember to call John"

# Note with tags
qnote add "Python logging best practices" -t python,dev

# Open in editor
qnote add --editor

# Note with title and tags
qnote add "Code review notes" --title "PR #123 Review" -t code-review
```

### qnote list

List all notes.

**Usage:**
```bash
qnote list [OPTIONS]
```

**Options:**
```
-t, --tags TEXT        Filter by tags (comma-separated)
--limit INTEGER        Maximum results (default: 50)
--sort [created|updated|title]  Sort order (default: updated)
--starred              Show only starred notes
```

**Examples:**
```bash
# List all notes
qnote list

# Filter by tag
qnote list --tags python

# Show only starred notes
qnote list --starred

# Limit and sort
qnote list --limit 10 --sort created
```

### qnote show

Display a specific note.

**Usage:**
```bash
qnote show NOTE_ID
```

**Examples:**
```bash
qnote show 42
```

### qnote edit

Edit an existing note in external editor.

**Usage:**
```bash
qnote edit NOTE_ID
```

**Examples:**
```bash
qnote edit 42
```

### qnote delete

Delete one or more notes.

**Usage:**
```bash
qnote delete [OPTIONS] NOTE_ID [NOTE_ID...]
```

**Options:**
```
-f, --force            Skip confirmation prompt
```

**Examples:**
```bash
# Delete single note (with confirmation)
qnote delete 42

# Delete multiple notes
qnote delete 1 2 3

# Skip confirmation
qnote delete 42 --force
```

### qnote search

Search through all content.

**Usage:**
```bash
qnote search [OPTIONS] QUERY
```

**Options:**
```
--type [note|snippet|todo|all]  Type to search (default: all)
-t, --tags TEXT                  Filter by tags
--limit INTEGER                  Maximum results (default: 50)
```

**Examples:**
```bash
# Search all content
qnote search "python"

# Search only snippets
qnote search "function" --type snippet

# Search with tag filter
qnote search "bug" --tags urgent
```

---

## Snippet Commands

### qnote snippet add

Add a code snippet.

**Usage:**
```bash
qnote snippet add [OPTIONS] [CODE]
```

**Options:**
```
-l, --language TEXT    Programming language
-t, --tags TEXT        Comma-separated tags
--title TEXT           Snippet title
--from-file PATH       Read code from file
--starred              Mark as starred
```

**Examples:**
```bash
# Simple snippet
qnote snippet add "print('hello')" -l python

# From file
qnote snippet add --from-file script.sh -l bash

# With title and tags
qnote snippet add "def hello(): pass" -l python --title "Hello function" -t examples
```

### qnote snippet list

List all code snippets.

**Usage:**
```bash
qnote snippet list [OPTIONS]
```

**Options:**
```
-l, --language TEXT    Filter by language
-t, --tags TEXT        Filter by tags
--starred              Show only starred snippets
--limit INTEGER        Maximum results (default: 50)
```

**Examples:**
```bash
# List all snippets
qnote snippet list

# Filter by language
qnote snippet list --language python

# Starred snippets only
qnote snippet list --starred
```

### qnote snippet show

Display a snippet with syntax highlighting.

**Usage:**
```bash
qnote snippet show SNIPPET_ID
```

**Examples:**
```bash
qnote snippet show 42
```

### qnote snippet edit

Edit a snippet in external editor.

**Usage:**
```bash
qnote snippet edit SNIPPET_ID
```

**Examples:**
```bash
qnote snippet edit 42
```

### qnote snippet delete

Delete one or more snippets.

**Usage:**
```bash
qnote snippet delete [OPTIONS] SNIPPET_ID [SNIPPET_ID...]
```

**Options:**
```
-f, --force            Skip confirmation
```

**Examples:**
```bash
qnote snippet delete 42
qnote snippet delete 1 2 3 --force
```

---

## TODO Commands

### qnote todo add

Create a new TODO item.

**Usage:**
```bash
qnote todo add [OPTIONS] TITLE
```

**Options:**
```
-p, --priority [low|medium|high]  Priority level (default: medium)
-d, --due DATE                     Due date (YYYY-MM-DD format)
--description TEXT                 Task description
-t, --tags TEXT                    Comma-separated tags
```

**Examples:**
```bash
# Simple TODO
qnote todo add "Review pull request"

# With priority and due date
qnote todo add "Release v2.0" -p high -d 2026-03-15

# With description
qnote todo add "Update docs" --description "Add API documentation section"
```

### qnote todo list

List TODO items.

**Usage:**
```bash
qnote todo list [OPTIONS]
```

**Options:**
```
--pending              Show only pending TODOs
--completed            Show only completed TODOs
-p, --priority [low|medium|high]  Filter by priority
-t, --tags TEXT        Filter by tags
--overdue              Show only overdue TODOs
--limit INTEGER        Maximum results (default: 50)
```

**Examples:**
```bash
# List all TODOs
qnote todo list

# Only pending
qnote todo list --pending

# High priority only
qnote todo list --priority high

# Overdue tasks
qnote todo list --overdue
```

### qnote todo show

Display a TODO item.

**Usage:**
```bash
qnote todo show TODO_ID
```

**Examples:**
```bash
qnote todo show 42
```

### qnote todo done

Mark a TODO as completed.

**Usage:**
```bash
qnote todo done TODO_ID
```

**Examples:**
```bash
qnote todo done 42
```

### qnote todo undone

Mark a TODO as not completed.

**Usage:**
```bash
qnote todo undone TODO_ID
```

**Examples:**
```bash
qnote todo undone 42
```

### qnote todo edit

Edit a TODO's description.

**Usage:**
```bash
qnote todo edit TODO_ID
```

**Examples:**
```bash
qnote todo edit 42
```

### qnote todo delete

Delete one or more TODOs.

**Usage:**
```bash
qnote todo delete [OPTIONS] TODO_ID [TODO_ID...]
```

**Options:**
```
-f, --force            Skip confirmation
```

**Examples:**
```bash
qnote todo delete 42
qnote todo delete 1 2 3 --force
```

---

## Configuration Commands

### qnote config list

Show current configuration.

**Usage:**
```bash
qnote config list
```

Displays all configuration values with their sources (config file or environment).

### qnote config get

Get a specific configuration value.

**Usage:**
```bash
qnote config get KEY
```

**Examples:**
```bash
# Get editor setting
qnote config get editor

# Get nested value
qnote config get sync.remote
```

### qnote config set

Set a configuration value.

**Usage:**
```bash
qnote config set KEY VALUE
```

**Examples:**
```bash
# Set editor
qnote config set editor nvim

# Set theme
qnote config set theme dark

# Set nested value
qnote config set sync.auto true
```

### qnote config reset

Reset configuration to defaults.

**Usage:**
```bash
qnote config reset
```

Creates a backup of current config and resets to defaults.

### qnote config path

Show path to configuration file.

**Usage:**
```bash
qnote config path
```

---

## Common Workflows

### Daily Note-Taking

```bash
# Quick note
qnote add "Meeting notes"

# Detailed note with editor
qnote add --editor -t meeting,work

# Review recent notes
qnote list --limit 10
```

### Code Snippet Management

```bash
# Save useful snippet
qnote snippet add "docker ps -a | grep Exit" -l bash

# Import from file
qnote snippet add --from-file ~/.bashrc -l bash

# Find snippet
qnote search "docker" --type snippet
```

### Task Management

```bash
# Create high-priority task
qnote todo add "Deploy to production" -p high -d 2026-02-15

# Check pending tasks
qnote todo list --pending

# Complete task
qnote todo done 1
```

## Exit Codes

- **0** - Success
- **1** - General error
- **2** - Invalid arguments
- **3** - Database error

## See Also

- [INSTALL.md](INSTALL.md) - Installation guide
- [CONFIG.md](CONFIG.md) - Configuration reference
- [COMPLETION.md](COMPLETION.md) - Shell completion
