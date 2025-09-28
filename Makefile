# Makefile for CLI Task Manager development

.PHONY: help install install-dev test lint format type-check quality clean build upload setup

# Default target
help:
	@echo "CLI Task Manager - Development Commands"
	@echo "======================================"
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup          - Set up development environment"
	@echo "  install        - Install production dependencies"
	@echo "  install-dev    - Install development dependencies"
	@echo ""
	@echo "Development Commands:"
	@echo "  run            - Run the application"
	@echo "  test           - Run tests"
	@echo "  test-cov       - Run tests with coverage"
	@echo "  lint           - Run linting (flake8)"
	@echo "  format         - Format code (black + isort)"
	@echo "  type-check     - Run type checking (mypy)"
	@echo "  quality        - Run all quality checks"
	@echo ""
	@echo "Build Commands:"
	@echo "  clean          - Clean build artifacts"
	@echo "  build          - Build package"
	@echo "  upload         - Upload to PyPI"
	@echo "  upload-test    - Upload to Test PyPI"
	@echo ""
	@echo "Other Commands:"
	@echo "  docs           - Generate documentation"
	@echo "  pre-commit     - Install pre-commit hooks"

# Setup development environment
setup:
	python -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  Windows: venv\\Scripts\\activate"
	@echo "  Unix:    source venv/bin/activate"
	@echo "Then run: make install-dev"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

# Run the application
run:
	python main.py

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=src --cov-report=html --cov-report=term

# Run linting
lint:
	flake8 src/ tests/

# Format code
format:
	black src/ tests/
	isort src/ tests/

# Run type checking
type-check:
	mypy src/

# Run all quality checks
quality: format lint type-check test

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	python -m build

# Upload to PyPI
upload: build
	twine upload dist/*

# Upload to Test PyPI
upload-test: build
	twine upload --repository testpypi dist/*

# Generate documentation
docs:
	@echo "Documentation generation not yet implemented"

# Install pre-commit hooks
pre-commit:
	pre-commit install

# Development shortcuts
dev: install-dev pre-commit
	@echo "Development environment ready!"

check: quality
	@echo "All quality checks passed!"
