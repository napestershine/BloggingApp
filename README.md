# Symfony Blog API

![CI](https://github.com/napestershine/sf5/workflows/CI/badge.svg)

A modern blog API built with Symfony 7.3 and API Platform, featuring JWT authentication, rich text editing with CKEditor, and a complete RESTful API for managing blog posts, users, and comments.

## 🚀 Features

- **Modern Symfony 7.3** framework with best practices
- **API Platform** integration for automatic API documentation and validation
- **JWT Authentication** for secure API access
- **Rich Text Editing** with CKEditor integration
- **User Management** with proper authentication and authorization
- **Blog Post Management** with CRUD operations
- **Comment System** for blog posts
- **Database Migrations** with Doctrine ORM
- **Data Fixtures** for development and testing
- **Code Quality Tools** (PHPStan, Rector)
- **Testing Setup** with PHPUnit

## 🛠 Technology Stack

- **Backend**: Symfony 7.3, PHP 8.2+
- **API**: API Platform 4.1
- **Database**: PostgreSQL (configurable)
- **Authentication**: JWT (LexikJWTAuthenticationBundle)
- **ORM**: Doctrine ORM 3.x
- **Template Engine**: Twig
- **Rich Text**: CKEditor Bundle
- **Testing**: PHPUnit
- **Code Quality**: PHPStan, Rector

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **PHP 8.2 or higher** with extensions:
  - `ext-ctype`
  - `ext-iconv`
- **Composer** (latest version)
- **PostgreSQL** (or MySQL/SQLite)
- **OpenSSL** for JWT key generation
- **Node.js & npm** (for CKEditor assets)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/napestershine/sf5.git
cd sf5
```

### 2. Install Dependencies

```bash
composer install
```

### 3. Environment Configuration

Copy the environment file and configure your settings:

```bash
cp .env .env.local
```

Edit `.env.local` and configure your database connection:

```env
# Database Configuration
DATABASE_URL="postgresql://username:password@127.0.0.1:5432/blog_db?serverVersion=15&charset=utf8"

# For MySQL use:
# DATABASE_URL="mysql://username:password@127.0.0.1:3306/blog_db?serverVersion=8.0.32&charset=utf8mb4"

# For SQLite use:
# DATABASE_URL="sqlite:///%kernel.project_dir%/var/data.db"

# Application Environment
APP_ENV=dev
APP_SECRET=your-secret-key-here
```

### 4. Database Setup

Create the database and run migrations:

```bash
# Create database
php bin/console doctrine:database:create

# Run migrations
php bin/console doctrine:migrations:migrate

# Load sample data (optional)
php bin/console doctrine:fixtures:load
```

### 5. JWT Configuration

Create the JWT directory and generate keys:

```bash
mkdir -p config/jwt
```

Generate JWT keys (you'll be prompted for a passphrase):

```bash
openssl genrsa -out config/jwt/private.pem -aes256 4096
openssl rsa -pubout -in config/jwt/private.pem -out config/jwt/public.pem
```

Add JWT configuration to your `.env.local`:

```env
###> lexik/jwt-authentication-bundle ###
JWT_SECRET_KEY=%kernel.project_dir%/config/jwt/private.pem
JWT_PUBLIC_KEY=%kernel.project_dir%/config/jwt/public.pem
JWT_PASSPHRASE=your-passphrase-here
###< lexik/jwt-authentication-bundle ###
```

### 6. Install CKEditor Assets

```bash
php bin/console ckeditor:install
php bin/console assets:install public
```

## 🏃‍♂️ Running the Application

### Development Server

Start the Symfony development server:

```bash
symfony server:start
```

Or use PHP's built-in server:

```bash
php -S localhost:8000 -t public/
```

The application will be available at `http://localhost:8000`

### API Documentation

Visit `http://localhost:8000/api` to access the API Platform documentation interface.

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
php bin/phpunit

# Run tests with coverage
php bin/phpunit --coverage-html var/coverage
```

## 🔍 Code Quality

### Static Analysis

```bash
# Run PHPStan
vendor/bin/phpstan analyse src tests

# Run Rector (dry-run)
vendor/bin/rector process --dry-run

# Apply Rector fixes
vendor/bin/rector process
```

## 📡 API Usage

### Authentication

First, create a user account:

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

Get an authentication token:

```bash
curl -X POST http://localhost:8000/api/login_check \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "secure_password"
  }'
```

### Blog Post Management

Create a blog post (requires authentication):

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

Get all blog posts:

```bash
curl -X GET http://localhost:8000/api/blog_posts
```

Get a specific blog post:

```bash
curl -X GET http://localhost:8000/api/blog_posts/1
```

### Alternative Endpoints

The application also provides traditional REST endpoints:

- `GET /blog` - List all blog posts with pagination
- `GET /blog/post/{id}` - Get blog post by ID
- `GET /blog/post/{slug}` - Get blog post by slug
- `POST /blog/add` - Create new blog post
- `DELETE /blog/post/{id}` - Delete blog post

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PSR-12 coding standards
- Write tests for new features
- Run code quality checks before committing
- Update documentation as needed

## 📝 License

This project is licensed under the Proprietary License.

## 🆘 Troubleshooting

### Common Issues

**JWT Configuration Issues:**
- Ensure JWT keys are generated correctly
- Check file permissions on JWT key files
- Verify the passphrase matches in your `.env.local`

**Database Connection Issues:**
- Verify database credentials in `.env.local`
- Ensure database server is running
- Check database exists and is accessible

**Asset Issues:**
- Run `php bin/console assets:install public`
- Clear cache with `php bin/console cache:clear`

**Permission Issues:**
- Ensure web server has read access to project files
- Check write permissions on `var/` directory

For more help, please open an issue in the GitHub repository.