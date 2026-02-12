# qnote(1) - Quick Note Manager

A minimalist command-line tool for managing notes, code snippets, and TODOs.

## NAME

qnote - terminal-based note and snippet manager

## SYNOPSIS

```
qnote [COMMAND] [OPTIONS] [ARGS...]
qnote add [OPTIONS] [CONTENT]
qnote list [OPTIONS]
qnote snippet SUBCOMMAND [OPTIONS]
qnote todo SUBCOMMAND [OPTIONS]
```

## DESCRIPTION

**qnote** is a lightweight CLI tool for managing notes, code snippets, and TODO items directly from your terminal. It stores data in a local SQLite database and supports tags, search, and external editor integration.

Features:
- Fast note-taking with optional editor integration
- Code snippet management with syntax highlighting
- TODO tracking with priorities and due dates
- Tag-based organization
- Full-text search across all content
- Shell completion (bash, zsh, fish)

## QUICK START

```bash
# Install from source
pip install -e .

# Or build and install .deb package
./build-deb.sh
sudo dpkg -i ../qnote_*.deb

# Create your first note
qnote add "My first note"

# List notes
qnote list

# Add a code snippet
qnote snippet add "print('hello')" -l python

# Create a TODO
qnote todo add "Task description" -p high
```

## INSTALLATION

See [docs/INSTALL.md](docs/INSTALL.md) for detailed installation instructions.

## DOCUMENTATION

Core documentation (read in order):
- [docs/INSTALL.md](docs/INSTALL.md) - Installation guide
- [docs/USAGE.md](docs/USAGE.md) - Command reference and examples
- [docs/CONFIG.md](docs/CONFIG.md) - Configuration options
- [docs/PACKAGING.md](docs/PACKAGING.md) - Building .deb packages

Additional topics:
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide
- [docs/COMPLETION.md](docs/COMPLETION.md) - Shell completion setup
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines
- [CHANGELOG.md](CHANGELOG.md) - Version history

## SHELL COMPLETION

qnote supports tab completion for bash, zsh, and fish.

```bash
# Bash
qnote --completion bash >> ~/.bashrc

# Zsh
qnote --completion zsh >> ~/.zshrc

# Fish
qnote --completion fish > ~/.config/fish/completions/qnote.fish
```

See [docs/COMPLETION.md](docs/COMPLETION.md) for details.

## FILES

```
~/.config/qnote/config.yaml    Configuration file
~/.local/share/qnote/qnote.db  SQLite database
```

## ENVIRONMENT

**EDITOR**
: Preferred editor for writing notes (default: vim)

**QNOTE_DB**
: Override database location

**QNOTE_CONFIG**
: Override config file location

## EXIT STATUS

- **0** - Success
- **1** - General error
- **2** - Invalid arguments
- **3** - Database error

## EXAMPLES

```bash
# Note management
qnote add "Quick note"
qnote add -t python,dev "Note with tags"
qnote add --editor
qnote list --tags python
qnote search "keyword"

# Code snippets
qnote snippet add "def hello(): print('hi')" -l python
qnote snippet add --from-file script.sh -l bash
qnote snippet list --language python

# TODOs
qnote todo add "Review PR" -p high -d 2026-03-15
qnote todo list --pending
qnote todo done 1

# Configuration
qnote config list
qnote config set editor nvim
qnote config get editor
```

## BUGS

Report bugs at: <https://github.com/olc1910/qnote/issues>

## AUTHOR

Written by Otis L. Crossley <qnote@olcrossley.uk>

## COPYRIGHT

Copyright (c) 2026 Otis L. Crossley. MIT License.

## SEE ALSO

git(1), sqlite3(1), vim(1)

Full documentation: <https://github.com/olc1910/qnote/blob/main/docs/>
