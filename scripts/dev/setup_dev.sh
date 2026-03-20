#!/bin/bash
set -e

echo "Setting up development environment..."

# Install dependencies
poetry install

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
fi

# Run database migrations
echo "Setup complete!"
