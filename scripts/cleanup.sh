#!/bin/bash

echo "Stopping and removing database container..."
docker compose down -v --remove-orphans

# Also remove any containers that might be stuck or not properly cleaned up
echo "Removing any remaining crafty containers..."
docker rm -f crafty-postgres 2>/dev/null || true

# Clean up any dangling containers related to this project
echo "Cleaning up any dangling containers..."
docker container prune -f