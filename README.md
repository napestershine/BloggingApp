# Symfony 5 Project

![CI](https://github.com/napestershine/sf5/workflows/CI/badge.svg)

## Setup

### Docker Setup (Recommended)

#### Quick Setup
Run the automated setup script:
```sh
./docker-setup.sh
```

#### Manual Setup
1. Copy the Docker environment configuration:
```sh
cp .env.docker .env.local
```

2. Generate JWT keys:
```sh
mkdir -p config/jwt
openssl genrsa -out config/jwt/private.pem -aes256 4096
openssl rsa -pubout -in config/jwt/private.pem -out config/jwt/public.pem
```

3. Start the Docker containers:
```sh
docker compose up -d
```

4. Install dependencies and setup database:
```sh
docker compose exec app composer install
docker compose exec app php bin/console doctrine:migrations:migrate
```

5. Access the application:
- **Web**: http://localhost:8080
- **API**: http://localhost:8080/api  
- **Database**: localhost:5432 (from host)

#### Useful Docker Commands
```sh
# Stop all services
docker compose down

# View logs
docker compose logs -f

# Access PHP container shell
docker compose exec app bash

# Run Symfony commands
docker compose exec app php bin/console cache:clear
```

### Manual Setup (Without Docker)

If you prefer not to use Docker, you can set up the project manually:

1. Install PHP 8.2+, PostgreSQL, and Composer
2. Copy environment configuration:
```sh
cp .env .env.local
```

3. Configure your database connection in `.env.local`

4. Generate JWT keys:
```sh
mkdir -p config/jwt
openssl genrsa -out config/jwt/private.pem -aes256 4096
openssl rsa -pubout -in config/jwt/private.pem -out config/jwt/public.pem
```

5. Install dependencies:
```sh
composer install
```

6. Run database migrations:
```sh
php bin/console doctrine:migrations:migrate
```

## Usage Examples

### Create a user
```json
{
    "username": "admin",
    "name": "Manu",
    "email": "manu@blog.com",
    "password": "123"
}
```

### Create a blog post
```json
{
    "title": "My First Post",
    "content": "This is the content of my first blog post.",
    "author": "admin"
}
```