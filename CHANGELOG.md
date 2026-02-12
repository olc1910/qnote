# Changelog

All notable changes to qnote will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Shell completion support (bash, zsh, fish)
- Comprehensive documentation in docs/ directory

## [0.1.0] - 2026-02-10

### Added
- Initial release
- Core note management (add, list, show, edit, delete)
- Code snippet management with syntax highlighting
- TODO tracking with priorities and due dates
- Tag-based organization
- Full-text search across all content types
- SQLite database backend
- External editor integration (vim, nano, vscode)
- Rich terminal UI with colors and tables
- YAML configuration system
- Debian package (.deb) support
- Comprehensive test suite
- Documentation (README, guides, man pages)

### Features
- **Notes**
  - Create notes with tags and titles
  - Edit in external editor
  - Star/favorite notes
  - List with filtering and sorting
  - Full-text search

- **Snippets**
  - Add code snippets with language detection
  - Import from files
  - Syntax highlighting
  - Filter by language and tags

- **TODOs**
  - Priority levels (low, medium, high)
  - Due dates
  - Mark as complete/incomplete
  - Filter by status, priority, tags
  - Show overdue items

- **Configuration**
  - YAML config file
  - Customizable editor, theme, pager
  - Environment variable support

- **Distribution**
  - .deb package for Debian/Ubuntu
  - pip installation support
  - Build scripts included

### Technical
- Python 3.8+ support
- Click for CLI framework
- Rich for terminal UI
- SQLite for data storage
- Pygments for syntax highlighting
- PyYAML for configuration
- pytest for testing
- Type hints throughout

## [0.0.1] - 2026-01-15

### Added
- Project structure
- Basic note functionality
- Database schema
- Initial documentation

---

## Release Notes

### Version 0.1.0 (Current)

First public release of qnote with full functionality for managing notes, code snippets, and TODOs from the terminal.

**Highlights:**
- Complete CLI tool ready for daily use
- Professional Debian packaging
- Comprehensive documentation
- Shell completion support
- Rich terminal interface
- Extensible architecture

**Installation:**
```bash
# From .deb package
sudo dpkg -i qnote_0.1.0-1_all.deb

# From source
pip install -e .
```

**Quick start:**
```bash
qnote add "My first note"
qnote snippet add "print('hello')" -l python
qnote todo add "Review code" -p high
```

See [README.md](README.md) and [docs/](docs/) for full documentation.

---

[Unreleased]: https://github.com/olc1910/qnote/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/olc1910/qnote/releases/tag/v0.1.0
[0.0.1]: https://github.com/olc1910/qnote/releases/tag/v0.0.1
