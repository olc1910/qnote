# Contributing to qnote

Thank you for considering contributing to qnote!

## How to Contribute

### Reporting Bugs

Report bugs at: <https://github.com/olc1910/qnote/issues>

Include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages

### Suggesting Features

Open an issue with:
- Clear description of the feature
- Why it would be useful
- Example use cases
- Proposed implementation (optional)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation
4. **Run tests**
   ```bash
   pytest
   black qnote tests
   flake8 qnote
   mypy qnote
   ```
5. **Commit your changes**
   ```bash
   git commit -m "feat: add new feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature
   ```
7. **Submit a pull request**

## Development Setup

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed setup instructions.

Quick start:
```bash
# Clone repository
git clone https://github.com/olc1910/qnote
cd qnote

# Install dependencies
pip install --user -e ".[dev]"

# Run tests
pytest
```

## Code Style

- Follow PEP 8
- Use type hints
- Line length: 100 characters
- Format with black
- Document with docstrings

Example:
```python
def function(param: str) -> int:
    """
    Brief description.
    
    Args:
        param: Description
    
    Returns:
        Description of return value
    """
    return 42
```

## Commit Messages

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

## Pull Request Guidelines

- One feature/fix per PR
- Include tests
- Update documentation
- Pass all checks (tests, linting, type checking)
- Update CHANGELOG.md

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=qnote

# Specific test
pytest tests/test_note.py
```

## Documentation

Update relevant documentation in `docs/`:
- INSTALL.md - Installation changes
- USAGE.md - New commands or options
- CONFIG.md - Configuration changes
- DEVELOPMENT.md - Development process changes

## Code of Conduct

- Be respectful and considerate
- Welcome newcomers
- Accept constructive criticism
- Focus on what is best for the project

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue or contact: qnote@olcrossley.uk

## See Also

- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide
- [docs/INSTALL.md](docs/INSTALL.md) - Installation guide
