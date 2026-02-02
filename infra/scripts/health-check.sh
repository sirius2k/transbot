#!/bin/bash

# TransBot Infrastructure Health Check Script

cd "$(dirname "$0")/.."

echo "🏥 Checking service health..."
echo ""

# Check PostgreSQL
if docker-compose ps postgres | grep -q "Up"; then
    if docker-compose exec -T postgres pg_isready -U transbot_user >/dev/null 2>&1; then
        echo "✅ PostgreSQL: Healthy"
    else
        echo "⚠️  PostgreSQL: Running but not ready"
    fi
else
    echo "❌ PostgreSQL: Not running"
fi

# Check Langfuse
if docker-compose ps langfuse | grep -q "Up"; then
    if curl -f -s http://localhost:3000/api/health >/dev/null 2>&1; then
        echo "✅ Langfuse: Healthy"
    else
        echo "⚠️  Langfuse: Starting up (this may take a minute)..."
    fi
else
    echo "❌ Langfuse: Not running"
fi

# Check Redis
if docker-compose ps redis | grep -q "Up"; then
    if docker-compose exec -T redis redis-cli -a "${REDIS_PASSWORD:-redis_password}" ping >/dev/null 2>&1; then
        echo "✅ Redis: Healthy"
    else
        echo "⚠️  Redis: Running but not ready"
    fi
else
    echo "❌ Redis: Not running"
fi

echo ""
