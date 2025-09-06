# Docker Setup for BloggingApp

This directory contains Docker configuration files to run the BloggingApp in containerized environments for end-to-end testing.

## Quick Start

### Development Environment

Run the full stack in development mode:

```bash
# Start both frontend and backend
docker compose -f docker-compose.dev.yml up

# Or start just the frontend for frontend-only testing
docker compose -f docker-compose.dev.yml up web

# Or start just the backend
docker compose -f docker-compose.dev.yml up api
```

The development setup includes:
- **Frontend**: Next.js app with hot reloading (port 3000)
- **Backend**: FastAPI with auto-reload (port 8000)
- **Database**: SQLite (for development)

### Production Environment

Run the full stack in production mode:

```bash
# Build and start all services
docker compose up --build

# Or start with PostgreSQL database
docker compose up --build api web db
```

The production setup includes:
- **Frontend**: Optimized Next.js build (port 3000)
- **Backend**: FastAPI production server (port 8000)
- **Database**: PostgreSQL (port 5432) + SQLite fallback

## Services

### Frontend (Next.js)
- **Development**: `./web/Dockerfile.dev` - includes hot reloading
- **Production**: `./web/Dockerfile` - optimized build with standalone output
- **Port**: 3000
- **Environment Variables**:
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