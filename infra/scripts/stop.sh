#!/bin/bash
set -e

# TransBot Infrastructure Stop Script
# Usage: ./stop.sh [service_name]
#   - No args: Stop all services
#   - service_name: Stop specific service (postgres, langfuse, redis)

cd "$(dirname "$0")/.."

echo "🛑 Stopping TransBot infrastructure..."

if [ -z "$1" ]; then
    echo "🔧 Stopping all services..."
    docker-compose down
else
    echo "🔧 Stopping $1..."
    docker-compose stop "$1"
fi

echo "✅ Services stopped successfully!"
