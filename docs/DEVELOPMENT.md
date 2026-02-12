# Development Guide

This document describes how to contribute to qnote development.

## Setup

### Clone Repository

```bash
git clone https://github.com/olc1910/qnote
cd qnote
```

### Development Installation

```bash
# Install in development mode with dev dependencies
pip install --user -e ".[dev]"

# Verify installation
qnote --version
```

### Development Dependencies

```bash
# Testing
pytest>=7.0.0
pytest-cov>=4.0.0

# Code quality
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
types-PyYAML
```

## Project Structure

```
qnote/
├── qnote/                  # Main package
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # Entry point
│   ├── cli.py              # CLI interface (Click)
│   ├── core/               # Core functionality
│   │   ├── database.py     # SQLite operations
│   │   ├── note.py         # Note CRUD
│   │   ├── snippet.py      # Snippet CRUD
│   │   └── todo.py         # TODO CRUD
│   ├── commands/           # Command implementations
│   │   ├── add.py          # Add commands
│   │   ├── list.py         # List commands
│   │   ├── show.py         # Show commands
│   │   ├── edit.py         # Edit commands
│   │   └── delete.py       # Delete commands
│   ├── utils/              # Utilities
│   │   ├── config.py       # Configuration management
│   │   ├── editor.py       # Editor integration
│   │   └── formatter.py    # Output formatting
│   └── sync/               # Sync functionality (future)
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_*.py           # Test modules
├── docs/                   # Documentation
│   ├── INSTALL.md
│   ├── USAGE.md
│   ├── CONFIG.md
│   ├── COMPLETION.md
│   ├── PACKAGING.md
│   └── DEVELOPMENT.md      # This file
├── debian/                 # Debian packaging
├── pyproject.toml          # Project metadata
├── setup.py                # Setup script
├── build-deb.sh            # Build script
└── README.md               # Main readme
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/new-command
```

### 2. Write Code

Follow the existing code structure:

```python
# In qnote/commands/mycommand.py
from rich.console import Console
from qnote.core.database import Database

console = Console()

def my_command(arg1: str, arg2: int) -> None:
    """
    Brief description.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    """
    db = Database()
    # Implementation
    console.print("[green]Success![/green]")
```

### 3. Add CLI Command

Register in `qnote/cli.py`:

```python
@main.command()
@click.argument("arg1")
@click.option("--arg2", type=int, default=0)
def mycommand(arg1: str, arg2: int) -> None:
    """
    Command description for --help output.
    
    Examples:
        qnote mycommand "value"
        qnote mycommand "value" --arg2 42
    """
    from qnote.commands.mycommand import my_command
    my_command(arg1, arg2)
```

### 4. Write Tests

```python
# In tests/test_mycommand.py
import pytest
from qnote.commands.mycommand import my_command

def test_my_command():
    """Test basic functionality"""
    result = my_command("test", 42)
    assert result is not None

def test_my_command_edge_case():
    """Test edge cases"""
    with pytest.raises(ValueError):
        my_command("", -1)
```

### 5. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=qnote

# Run specific test
pytest tests/test_mycommand.py

# Run with verbose output
pytest -v
```

### 6. Format Code

```bash
# Format with black
black qnote tests

# Check with flake8
flake8 qnote

# Type check with mypy
mypy qnote
```

### 7. Commit Changes

```bash
git add .
git commit -m "feat: add new command

- Implement mycommand functionality
- Add tests
- Update documentation"
```

## Code Style

### Python Style

Follow PEP 8 with these specifics:

```python
# Line length: 100 characters
# Use type hints
def function(param: str) -> int:
    """Docstring with description."""
    return 42

# Use f-strings for formatting
message = f"Value: {value}"

# Use pathlib for paths
from pathlib import Path
config_path = Path.home() / ".config" / "qnote"
```

### Docstrings

Use Google-style docstrings:

```python
def function(arg1: str, arg2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When arg1 is empty
    """
    pass
```

### Import Order

```python
# Standard library
import os
from pathlib import Path

# Third-party
import click
from rich.console import Console

# Local
from qnote.core.database import Database
from qnote.utils.config import Config
```

## Testing

### Test Structure

```python
# tests/test_note.py
import pytest
from qnote.core.note import Note
from qnote.core.database import Database

@pytest.fixture
def db():
    """Create temporary database for testing"""
    db = Database(":memory:")
    yield db
    db.close()

def test_note_creation(db):
    """Test creating a note"""
    note = Note(db)
    result = note.create("Test content")
    assert result is not None
```

### Running Tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=qnote --cov-report=html

# Specific file
pytest tests/test_note.py

# Specific test
pytest tests/test_note.py::test_note_creation

# With output
pytest -v -s
```

### Coverage

```bash
# Generate coverage report
pytest --cov=qnote --cov-report=html

# View report
xdg-open htmlcov/index.html
```

## Building and Testing Packages

### Build Package

```bash
# Clean previous builds
./cleanup-project.sh

# Build .deb package
./build-deb.sh

# Test installation in Docker
docker run -it debian:latest bash
# Inside container:
apt update && apt install -y /path/to/qnote_*.deb
qnote --version
```

### Manual Testing

```bash
# Install development version
pip install --user -e .

# Test commands
qnote add "test note"
qnote list
qnote snippet add "print('test')" -l python
qnote todo add "test task"

# Check database
sqlite3 ~/.local/share/qnote/qnote.db ".tables"
```

## Database Schema

SQLite schema:

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    title TEXT,
    tags TEXT,
    starred BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE snippets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    language TEXT,
    title TEXT,
    description TEXT,
    tags TEXT,
    starred BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'medium',
    due_date DATE,
    completed BOOLEAN DEFAULT 0,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Adding New Features

### Example: Add "archive" Command

1. Create command file:

```python
# qnote/commands/archive.py
from rich.console import Console
from qnote.core.database import Database

console = Console()

def archive_note(note_id: int) -> None:
    """Archive a note"""
    db = Database()
    # Implementation
    console.print(f"[green]Note {note_id} archived[/green]")
```

2. Add to CLI:

```python
# qnote/cli.py
@main.command()
@click.argument("note_id", type=int)
def archive(note_id: int) -> None:
    """Archive a note"""
    from qnote.commands.archive import archive_note
    archive_note(note_id)
```

3. Write tests:

```python
# tests/test_archive.py
def test_archive_note():
    """Test archiving a note"""
    # Test implementation
    pass
```

4. Update documentation:

```markdown
# docs/USAGE.md
### qnote archive

Archive a note.

**Usage:**
qnote archive NOTE_ID
```

## Debugging

### Enable Debug Mode

```python
# In commands
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use Rich console
from rich.console import Console
console = Console(log_path=True)
console.log("Debug message")
```

### Database Inspection

```bash
# Open database
sqlite3 ~/.local/share/qnote/qnote.db

# List tables
.tables

# Query notes
SELECT * FROM notes;

# Check schema
.schema notes
```

### Common Issues

**Import errors:**
```bash
# Reinstall in development mode
pip install --user -e .
```

**Database locked:**
```bash
# Close any open connections
rm ~/.local/share/qnote/qnote.db-journal
```

## Contributing

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Run tests and linters
7. Submit pull request

### Commit Messages

Follow conventional commits:

```
feat: add new feature
fix: fix bug
docs: update documentation
test: add tests
refactor: refactor code
style: format code
chore: update dependencies
```

### Code Review

All changes require:
- Tests passing
- Code formatted (black)
- Linters passing (flake8, mypy)
- Documentation updated
- Changelog updated

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Update `debian/changelog`
4. Build and test package
5. Tag release: `git tag v0.2.0`
6. Push: `git push --tags`
7. Create GitHub release
8. Upload .deb package

## See Also

- [INSTALL.md](INSTALL.md) - Installation guide
- [USAGE.md](USAGE.md) - Command reference
- [PACKAGING.md](PACKAGING.md) - Package building
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contributing guidelines
