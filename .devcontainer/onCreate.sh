#!/bin/bash

set -e

echo "Setting up development environment..."

# Sync Python dependencies
echo "Installing Python dependencies..."
uv sync --all-extras --quiet --dev --frozen

# Register Jupyter kernel
echo "Registering Jupyter kernel..."
uv run python -m ipykernel install --user --name mineria-datos --display-name "Python 3.13 (mineria-datos)"

# Install pre-commit hooks
# Los hooks de pre-commit NO se instalan a proposito: los alumnos trabajan en este
# mismo Codespace, y un hook que reescribe archivos hace fallar su primer commit sin
# que entiendan por que. Quien los quiera: `just pre-commit-install`.
