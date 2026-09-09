# justfile for Minería de Datos ITAM course

# Set shell for all recipes
set shell := ["bash", "-c"]

# Default recipe (show help)
default:
    @just --list

# Install Python dependencies with uv
install:
    uv sync --locked

# Install with dev dependencies
install-dev:
    uv sync --locked --group dev

# Preview the Quarto book locally
preview:
    uv run quarto preview chapters

# Render the complete book to HTML
render:
    uv run quarto render chapters

# Clean generated files
clean:
    rm -rf chapters/_freeze
    rm -rf chapters/.quarto
    rm -rf docs
    rm -rf .quarto
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

# Format Python code (ruff lee .ipynb de forma nativa, sin nbqa)
format:
    uv run ruff format .

# Run pre-commit hooks on all files
pre-commit:
    uv run pre-commit run --all-files

# Install pre-commit git hooks
pre-commit-install:
    uv run pre-commit install

# Update uv.lock file
lock:
    uv lock

# Sync dependencies (install + update if needed)
sync:
    uv sync

# Check for outdated dependencies
outdated:
    uv tree --outdated

# Run Jupyter Lab
lab:
    uv run jupyter lab

# Run Jupyter Notebook
notebook:
    uv run jupyter notebook

# Execute a specific notebook (usage: just execute notebooks/intro.ipynb)
execute FILE:
    uv run jupyter nbconvert --to notebook --execute --inplace {{FILE}}

# Execute all notebooks
execute-all:
    #!/usr/bin/env bash
    for notebook in notebooks/*.ipynb; do
        echo "Executing $notebook..."
        uv run jupyter nbconvert --to notebook --execute --inplace "$notebook"
    done

# Clear notebook outputs (useful before committing)
clear-outputs:
    #!/usr/bin/env bash
    for notebook in notebooks/*.ipynb; do
        echo "Clearing outputs in $notebook..."
        uv run jupyter nbconvert --clear-output --inplace "$notebook"
    done

# Full build pipeline: format, render
build: format render

# Development setup: install everything and setup hooks
setup: install-dev pre-commit-install
    @echo "Development environment ready!"
    @echo "Run 'just preview' to start the preview server"

# Check Python version
check-python:
    @python --version
    @which python

# Show uv cache info
cache-info:
    uv cache dir
    uv cache size

# Clean uv cache
cache-clean:
    uv cache clean
