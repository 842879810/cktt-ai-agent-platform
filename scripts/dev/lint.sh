#!/bin/bash
set -e

echo "Running linters..."

poetry run ruff check .
poetry run black --check .

echo "Linting complete!"
