# Symfony Blog API

![CI](https://github.com/napestershine/sf5/workflows/CI/badge.svg)

## Setup

### Docker Setup (Recommended)

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
docker-compose up -d
```

4. Install dependencies and setup database:
```sh
docker-compose exec app composer install
docker-compose exec app php bin/console doctrine:migrations:migrate
```

5. Access the application:
- API: http://localhost:8080
- Database: localhost:5432 (from host)

### Manual Setup

### JWT Keys Generation
```sh
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