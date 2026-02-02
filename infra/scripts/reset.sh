#!/bin/bash
set -e

# TransBot Infrastructure Reset Script
# ⚠️  WARNING: This will DELETE ALL DATA in volumes!

cd "$(dirname "$0")/.."

echo "⚠️  WARNING: This will DELETE ALL DATA!"
echo ""
echo "This will:"
echo "  - Stop all services"
echo "  - Remove all containers"
echo "  - Delete all volumes (PostgreSQL, Redis data)"
echo ""
read -p "Are you sure? (type 'yes' to confirm): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Reset cancelled"
    exit 1
fi

echo ""
echo "🗑️  Stopping and removing services..."
docker-compose down -v

echo "🧹 Cleaning up volumes..."
docker volume rm transbot_postgres_data 2>/dev/null || true
docker volume rm transbot_redis_data 2>/dev/null || true

echo "✅ Reset complete! Run ./start.sh to restart services."
