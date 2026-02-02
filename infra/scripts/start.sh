#!/bin/bash
set -e

# TransBot Infrastructure Startup Script
# Usage: ./start.sh [service_name]
#   - No args: Start all services
#   - service_name: Start specific service (postgres, langfuse, redis)

cd "$(dirname "$0")/.."

echo "🚀 Starting TransBot infrastructure..."

# Check if .env.infra exists
if [ ! -f .env.infra ]; then
    echo "⚠️  .env.infra not found. Creating from template..."
    cp .env.infra.example .env.infra
    echo "📝 Please edit .env.infra and set your passwords!"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit..."
fi

# Load environment variables
export $(cat .env.infra | grep -v '^#' | xargs)

# Start services
if [ -z "$1" ]; then
    echo "🔧 Starting all services..."
    docker-compose --env-file .env.infra up -d
else
    echo "🔧 Starting $1..."
    docker-compose --env-file .env.infra up -d "$1"
fi

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Health check
./scripts/health-check.sh

echo ""
echo "✅ Infrastructure is ready!"
echo ""
echo "📊 Service URLs:"
echo "   - Langfuse:   http://localhost:${LANGFUSE_PORT:-3000}"
echo "   - PostgreSQL: localhost:${POSTGRES_PORT:-5432}"
echo "   - Redis:      localhost:${REDIS_PORT:-6379}"
echo ""
echo "📝 Next steps:"
echo "   1. Open Langfuse and create a new project"
echo "   2. Copy API keys to TransBot .env file"
echo "   3. Run: streamlit run app.py"
echo ""
