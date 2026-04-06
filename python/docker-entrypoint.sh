#!/bin/bash
set -e

echo "🐳 Starting BloggingApp Python backend..."

# Run database migrations using the repo's canonical Alembic config.
if [ -f "alembic.ini" ]; then
    echo "📊 Running database migrations..."
    alembic -c alembic.ini upgrade head
fi

# Optional seeding for development
if [ "$SEED_ON_START" = "true" ]; then
    echo "🌱 Running database seeding..."
    python seed.py up
    echo "✅ Database seeding completed"
fi

echo "🚀 Starting application..."
exec "$@"
