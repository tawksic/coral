#!/bin/bash

# Local CI simulation script
# This mimics what GitHub Actions will do

set -e

echo "Starting local CI simulation..."

# Stage 1: Install Dependencies
echo "Installing dependencies..."
if uv sync --group dev; then
    echo "PASS: Dependencies installed successfully"
else
    echo "FAIL: Failed to install dependencies"
    exit 1
fi

# Stage 2: Lint
echo "Running linter..."
if uv run python -m flake8 app/ --extend-ignore=E302,E501,W391; then
    echo "PASS: Linting passed"
else
    echo "FAIL: Linting failed"
    exit 1
fi

# Stage 3: Test
echo "Running tests..."
if uv run python -m pytest tests/ -v --tb=short; then
    echo "PASS: All tests passed"
else
    echo "FAIL: Tests failed"
    exit 1
fi

echo ""
