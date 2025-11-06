#!/bin/bash
# Build script for Ludicé Docker images

set -e

echo "🏗️  Building Ludicé Docker Images..."

# Build backend
echo "📦 Building backend..."
docker build -t ludice-backend:latest -f backend/Dockerfile backend/

# Build frontend (bot)
echo "🤖 Building bot..."
docker build -t ludice-bot:latest -f frontend/Dockerfile .

# Build Go Redis service
echo "⚡ Building Redis service..."
docker build -t ludice-redis-service:latest -f backend/redis/Dockerfile backend/redis/

echo "✅ All images built successfully!"
echo ""
echo "To run the stack:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
