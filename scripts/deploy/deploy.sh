#!/bin/bash
set -e

echo "Deploying application..."

# Build Docker images
docker-compose build

# Start services
docker-compose up -d

echo "Deployment complete!"
