Here’s a cleaned-up, conflict-free README that merges both versions and keeps everything consistent with Symfony **7.3** and your stack.

---

# Symfony Blog API

![CI](https://github.com/napestershine/sf5/workflows/CI/badge.svg)

A modern blog API built with Symfony 7.3 and API Platform, featuring JWT authentication, rich text editing with CKEditor, and a complete RESTful API for managing blog posts, users, and comments.

## 🚀 Features

* **Modern Symfony 7.3** framework with best practices
* **API Platform** integration for automatic API documentation and validation
* **JWT Authentication** for secure API access
* **Rich Text Editing** with CKEditor integration
* **User Management** with proper authentication and authorization
* **Blog Post Management** with CRUD operations
* **Comment System** for blog posts
* **Database Migrations** with Doctrine ORM
* **Data Fixtures** for development and testing
* **Code Quality Tools** (PHPStan, Rector)
* **Testing Setup** with PHPUnit

## 🛠 Technology Stack

* **Backend**: Symfony 7.3, PHP 8.2+
* **API**: API Platform 4.1
* **Database**: PostgreSQL (configurable)
* **Authentication**: JWT (LexikJWTAuthenticationBundle)
* **ORM**: Doctrine ORM 3.x
* **Template Engine**: Twig
* **Rich Text**: CKEditor Bundle
* **Testing**: PHPUnit
* **Code Quality**: PHPStan, Rector

## 📋 Prerequisites

* **PHP 8.2 or higher** with:

  * `ext-ctype`
  * `ext-iconv`
* **Composer** (latest)
* **OpenSSL** (for JWT key generation)
* **PostgreSQL** (or MySQL/SQLite)
* **Node.js & npm** (for CKEditor assets)
* **Docker & Docker Compose** (optional, recommended)

---

## 🐳 Docker Setup (Recommended)

### Quick Setup

```sh
./docker-setup.sh
```

### Manual Setup

1. Copy Docker environment:

```sh
cp .env.docker .env.local
```

2. Generate JWT keys:

```sh
mkdir -p config/jwt
openssl genrsa -out config/jwt/private.pem -aes256 4096
openssl rsa -pubout -in config/jwt/private.pem -out config/jwt/public.pem
```

3. Start containers:

```sh
docker compose up -d
```

4. Install dependencies & run migrations:

```sh
docker compose exec app composer install
docker compose exec app php bin/console doctrine:migrations:migrate
# (Optional) fixtures
docker compose exec app php bin/console doctrine:fixtures:load
```

5. Access:

* **Web**: [http://localhost:8080](http://localhost:8080)
* **API Docs**: [http://localhost:8080/api](http://localhost:8080/api)
* **Database**: localhost:5432 (from host)

**Useful Docker Commands**

```sh
docker compose down
docker compose logs -f
docker compose exec app bash
docker compose exec app php bin/console cache:clear
```

---

## 🧰 Manual Setup (Without Docker)

### 1) Clone

```bash
git clone https://github.com/napestershine/sf5.git
cd sf5
```

### 2) Install dependencies

```bash
composer install
```

### 3) Environment

```bash
cp .env .env.local
```

Edit `.env.local`:

```env
# Database Configuration
DATABASE_URL="postgresql://username:password@127.0.0.1:5432/blog_db?serverVersion=15&charset=utf8"

# For MySQL:
# DATABASE_URL="mysql://username:password@127.0.0.1:3306/blog_db?serverVersion=8.0.32&charset=utf8mb4"

# For SQLite:
# DATABASE_URL="sqlite:///%kernel.project_dir%/var/data.db"

APP_ENV=dev
APP_SECRET=your-secret-key-here
```

### 4) Database

```bash
php bin/console doctrine:database:create
php bin/console doctrine:migrations:migrate
# Optional sample data
php bin/console doctrine:fixtures:load
```

### 5) JWT Configuration

Create keys:

```bash
mkdir -p config/jwt
openssl genrsa -out config/jwt/private.pem -aes256 4096
openssl rsa -pubout -in config/jwt/private.pem -out config/jwt/public.pem
```

Add to `.env.local`:

```env
###> lexik/jwt-authentication-bundle ###
JWT_SECRET_KEY=%kernel.project_dir%/config/jwt/private.pem
JWT_PUBLIC_KEY=%kernel.project_dir%/config/jwt/public.pem
JWT_PASSPHRASE=your-passphrase-here
###< lexik/jwt-authentication-bundle ###
```

### 6) CKEditor Assets

```bash
php bin/console ckeditor:install
php bin/console assets:install public
```

---

## 🏃‍♂️ Running the Application

### Symfony CLI

```bash
symfony server:start
```

### Or PHP built-in server

```bash
php -S localhost:8000 -t public/
```

* App: `http://localhost:8000`
* API Docs: `http://localhost:8000/api`

---

## 🧪 Testing

```bash
# Run all tests
php bin/phpunit

# With coverage
php bin/phpunit --coverage-html var/coverage
```

---

## 🔍 Code Quality

```bash
# PHPStan
vendor/bin/phpstan analyse src tests

# Rector (dry-run)
vendor/bin/rector process --dry-run

# Apply Rector fixes
vendor/bin/rector process
```

---

## 📡 API Usage

### Authentication

Create a user:

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "secure_password"
  }'
```

Get a token:

```bash
curl -X POST http://localhost:8000/api/login_check \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "secure_password"
  }'
```

### Blog Posts

Create (requires Bearer token):

```bash
curl -X POST http://localhost:8000/api/blog_posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my blog post...",
    "slug": "my-first-blog-post"
  }'
```

List:

```bash
curl -X GET http://localhost:8000/api/blog_posts
```

Get by ID:

```bash
curl -X GET http://localhost:8000/api/blog_posts/1
```

### Alternative Endpoints

* `GET /blog` — List with pagination
* `GET /blog/post/{id}` — By ID
* `GET /blog/post/{slug}` — By slug
* `POST /blog/add` — Create
* `DELETE /blog/post/{id}` — Delete

---

## 📁 Project Structure

```
src/
├── Controller/          # HTTP controllers
├── Entity/              # Doctrine entities
├── Repository/          # Data repositories
├── DataFixtures/        # Sample data
├── EventSubscriber/     # Event listeners
└── Migrations/          # Database migrations

config/
├── packages/            # Bundle configurations
├── routes/              # Routing configuration
└── jwt/                 # JWT keys

templates/               # Twig templates
tests/                   # Test files
public/                  # Web accessible files
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit (`git commit -m 'Add some amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Guidelines**

* Follow PSR-12 coding standards
* Write tests for new features
* Run code quality checks before committing
* Update documentation as needed

---

## 📝 License

This project is licensed under the Proprietary License.

---

## 🆘 Troubleshooting

**JWT Issues**

* Ensure keys are generated and readable
* Confirm passphrase matches `.env.local`
* Check file permissions on `config/jwt/*`

**Database Issues**

* Verify credentials and server status
* Ensure the database exists and is accessible
* Re-run migrations as needed

**Assets**

* Run `php bin/console assets:install public`
* Clear cache: `php bin/console cache:clear`

**Permissions**

* Web server must read project files
* `var/` must be writable

For more help, please open an issue in the GitHub repository.
