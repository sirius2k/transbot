#!/bin/bash

# TransBot Infrastructure Logs Script
# Usage: ./logs.sh [service_name] [-f]
#   - No args: Show all logs
#   - service_name: Show specific service logs (postgres, langfuse, redis)
#   - -f: Follow logs (live tail)

cd "$(dirname "$0")/.."

if [ "$1" == "-f" ] || [ "$2" == "-f" ]; then
    FOLLOW_FLAG="-f"
else
    FOLLOW_FLAG=""
fi

if [ -z "$1" ] || [ "$1" == "-f" ]; then
    echo "📋 Showing logs from all services..."
    docker-compose logs $FOLLOW_FLAG
else
    echo "📋 Showing logs from $1..."
    docker-compose logs $FOLLOW_FLAG "$1"
fi
