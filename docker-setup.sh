#!/bin/bash
set -e

echo "🐳 Setting up Symfony with Docker..."

# Copy Docker environment configuration
if [ ! -f .env.local ]; then
    echo "📋 Copying Docker environment configuration..."
    cp .env.docker .env.local
fi

# Generate JWT keys if they don't exist
if [ ! -f config/jwt/private.pem ]; then
    echo "🔐 Generating JWT keys..."
    mkdir -p config/jwt
    echo "Please enter a passphrase for JWT keys (or press Enter for default):"
    read -s passphrase
    if [ -z "$passphrase" ]; then
        passphrase="your_passphrase_here"
    fi
    
    openssl genrsa -out config/jwt/private.pem -aes256 -passout pass:"$passphrase" 4096
    openssl rsa -pubout -in config/jwt/private.pem -out config/jwt/public.pem -passin pass:"$passphrase"
    
    # Update the passphrase in .env.local
    sed -i "s/JWT_PASSPHRASE=your_passphrase_here/JWT_PASSPHRASE=$passphrase/" .env.local
fi

echo "🚀 Starting Docker containers..."
docker compose up -d

echo "📦 Installing dependencies..."
docker compose exec app composer install --no-interaction

echo "🗄️  Setting up database..."
docker compose exec app php bin/console doctrine:database:create --if-not-exists
docker compose exec app php bin/console doctrine:migrations:migrate --no-interaction

echo "✅ Setup complete!"
echo ""
echo "🌐 Your application is now running:"
echo "   - Web: http://localhost:8080"
echo "   - API: http://localhost:8080/api"
echo "   - Database: localhost:5432"
echo ""
echo "🛠️  Useful commands:"
echo "   - Stop:    docker compose down"
echo "   - Logs:    docker compose logs -f"
echo "   - Shell:   docker compose exec app bash"
echo ""