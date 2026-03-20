#!/bin/bash
set -e

echo "Checking health..."

# Check API health
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$response" = "200" ]; then
    echo "Health check passed!"
    exit 0
else
    echo "Health check failed!"
    exit 1
fi
