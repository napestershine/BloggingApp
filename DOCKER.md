# Docker Setup Guide

This guide explains the consolidated Docker setup for BloggingApp with profile-driven configurations.

## Quick Start

### Development (with hot reload)
```bash
# Using Makefile (recommended)
make up-dev

# Or manually
docker compose -f compose.yml -f compose.dev.yml up --build
```

### Production
```bash
# Using Makefile
make up

# Or manually  
docker compose up --build -d
```

### Testing
```bash
# Using Makefile
make test

# Or manually
docker compose -f compose.yml -f compose.ci.yml up --build --abort-on-container-exit
```

## Environment Configuration

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:
   ```bash
   # Database settings
   POSTGRES_DB=blog_db
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   
   # API settings
   SECRET_KEY=your-secret-key-change-in-production
   
   # Web settings
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

## Architecture

### Multi-stage Dockerfiles

**API (python/Dockerfile)**:
- `base`: Python 3.12 with system dependencies
- `deps`: Install Python packages with pip caching
- `dev`: Development stage with hot reload
- `prod`: Production stage with non-root user

**Web (web/Dockerfile)**:
- `deps`: Install Node.js dependencies with npm caching
- `builder`: Build Next.js application
- `runner`: Production runtime with standalone output

### Services

| Service | Purpose | Ports | Health Check |
|---------|---------|--------|--------------|
| `db` | PostgreSQL 16 database | 5432 | `pg_isready` |
| `api` | FastAPI backend | 8000 | `/health` endpoint |
| `web` | Next.js frontend | 3000 | `/api/health` endpoint |

### Profiles and Overrides

**Development (`compose.dev.yml`)**:
- Bind mounts for live code reloading
- Development build targets
- Verbose logging
- Development database

**Production (default `compose.yml`)**:
- Optimized production images
- No bind mounts
- Minimal logging
- Production database with persistence

**CI/Testing (`compose.ci.yml`)**:
- Test database (in-memory)
- Test commands instead of servers
- No persistent volumes

## Common Commands

### Service Management
```bash
# Start development environment
make up-dev

# Start production environment
make up

# Stop all services
make down

# Restart services
make rebuild
```

### Logs and Monitoring
```bash
# View all logs
make logs

# View specific service logs
make logs-api
make logs-web
make logs-db

# Check service health
make health

# Check service status
make status
```

### Database Operations
```bash
# Connect to database shell
make db-shell

# Backup database
make db-backup

# Seed database with demo data
docker compose exec api python seed.py up
```

### Development
```bash
# Open shell in API container
make shell-api

# Open shell in Web container
make shell-web

# Run tests
make test
make test-api
make test-web
```

### Cleanup
```bash
# Remove stopped containers and unused images
make clean

# Remove everything (DESTRUCTIVE)
make clean-all
```

## Security Features

- **Non-root users**: Production containers run as dedicated users
- **Secret management**: No secrets baked into images
- **Network isolation**: Services communicate through named networks
- **Health checks**: All services have health monitoring
- **Multi-stage builds**: Minimal production image sizes

## Performance Optimizations

- **BuildKit**: Enabled for parallel builds and caching
- **Layer caching**: Efficient caching for npm and pip
- **Standalone builds**: Next.js standalone output for smaller images
- **Multi-stage**: Separate build and runtime environments

## Troubleshooting

### Build Issues
```bash
# Clear all caches and rebuild
docker system prune -af
docker compose build --no-cache

# Check BuildKit is enabled
export DOCKER_BUILDKIT=1
```

### Network Issues
```bash
# Check service connectivity
docker compose exec api ping web
docker compose exec web ping api
docker compose exec api ping db
```

### Database Issues
```bash
# Check database logs
make logs-db

# Test database connection
docker compose exec api python -c "from app.database import engine; print(engine.execute('SELECT 1').scalar())"
```

### Permission Issues
```bash
# Fix file permissions (if needed)
sudo chown -R $USER:$USER .
```

## Flutter CI (Optional)

For CI builds of the Flutter mobile app:

```bash
# Build Flutter CI image
docker build -f infra/docker/Dockerfile.flutter.ci -t blogging-app-flutter-ci .

# Run Flutter tests
docker run --rm -v $(pwd)/app:/workspace blogging-app-flutter-ci flutter test
```

Note: Flutter is not included in the default compose setup. Use the CI Dockerfile only for automated testing of the mobile app.
  - `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
  - `NEXT_PUBLIC_SITE_URL`: Frontend URL (default: http://localhost:3000)

### Backend (FastAPI)
- **File**: `./python/Dockerfile`
- **Port**: 8000
- **Environment Variables**:
  - `DATABASE_URL`: Database connection string
  - `SECRET_KEY`: JWT secret key
  - `CORS_ORIGINS`: Allowed CORS origins

### Database (PostgreSQL)
- **Image**: `postgres:15-alpine`
- **Port**: 5432
- **Environment Variables**:
  - `POSTGRES_DB`: blog_db
  - `POSTGRES_USER`: user
  - `POSTGRES_PASSWORD`: password

## End-to-End Testing

The Docker setup enables several testing scenarios:

### 1. Full Stack Testing
```bash
docker compose up
# Access frontend at http://localhost:3000
# API documentation at http://localhost:8000/docs
```

### 2. Frontend Only Testing
```bash
docker compose up web
# Access frontend at http://localhost:3000
# Note: API calls will fail without backend
```

### 3. Backend Only Testing
```bash
docker compose up api
# API available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### 4. Development with Hot Reloading
```bash
docker compose -f docker-compose.dev.yml up
# Both frontend and backend will auto-reload on file changes
```

## Networking

All services run in a shared Docker network (`blogging-network`) allowing:
- Frontend to communicate with backend via container names
- Backend to communicate with database
- External access via mapped ports

## Volume Mounts

### Development Mode
- Frontend: `./web:/app` - source code sync for hot reloading
- Backend: `./python:/app` - source code sync for auto-reload

### Production Mode
- Database: `postgres_data:/var/lib/postgresql/data` - persistent storage

## Environment Configuration

### Frontend Environment Variables

Create `.env.local` in the `web` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

### Backend Environment Variables

Already configured in `docker-compose.yml`:
```env
DATABASE_URL=sqlite:///./blog.db
SECRET_KEY=your-secret-key-here-change-in-production
CORS_ORIGINS=http://localhost:3000
```

## Troubleshooting

### Port Conflicts
If ports 3000 or 8000 are in use, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Use port 3001 instead of 3000
```

### Database Issues
- SQLite: Data stored in `./python/blog.db`
- PostgreSQL: Data stored in Docker volume `postgres_data`

### Build Issues
Clean rebuild all containers:
```bash
docker compose down
docker compose build --no-cache
docker compose up
```

### Development Hot Reloading
If changes aren't reflected:
1. Ensure volume mounts are working
2. Check file permissions
3. Restart the development containers

## Production Deployment

For production deployment:

1. Update environment variables in `docker-compose.yml`
2. Use proper secrets management
3. Configure reverse proxy (nginx) if needed
4. Set up proper SSL certificates
5. Configure database backups

## Next Steps

- Add nginx reverse proxy configuration
- Add SSL/TLS termination
- Add monitoring and logging
- Add backup strategies
- Add CI/CD pipeline integration