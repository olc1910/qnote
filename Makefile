# Makefile for qnote development

.PHONY: help install install-dev test lint format clean build upload deb

help:
	@echo "qnote - Development Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make install       Install package in editable mode"
	@echo "  make install-dev   Install with development dependencies"
	@echo "  make test          Run tests with pytest"
	@echo "  make lint          Run linters (flake8, mypy)"
	@echo "  make format        Format code with black"
	@echo "  make check         Run all checks (format, lint, test)"
	@echo "  make clean         Remove build artifacts"
	@echo "  make build         Build distribution packages"
	@echo "  make deb           Build Debian package"
	@echo "  make upload        Upload to PyPI (requires credentials)"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,sync,clipboard]"

test:
	pytest --cov=qnote --cov-report=html --cov-report=term-missing

lint:
	flake8 qnote
	mypy qnote

format:
	black qnote tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

deb: clean
	./build-deb.sh

upload: build
	python -m twine upload dist/*

# Development workflow
dev: install-dev
	@echo "Development environment ready!"
	@echo "Run 'qnote --version' to verify installation"

# Run a quick sanity check
check: format lint test
	@echo "All checks passed!"
