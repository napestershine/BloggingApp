# BloggingApp Documentation

Welcome to the comprehensive documentation for **BloggingApp** - a modern, full-stack blogging platform featuring a Flutter mobile application, Next.js web application, and FastAPI backend.

## Architecture Overview

BloggingApp follows a monorepo structure with three main applications:

```
BloggingApp/
├── apps/
│   ├── api/          # FastAPI backend with JWT auth
│   ├── web/          # Next.js TypeScript frontend
│   └── mobile/       # Flutter mobile application
├── infra/
│   └── docker/       # Docker configurations
└── docs/             # Documentation
```

## Key Features

- ✅ **User Authentication**: JWT-based security with registration and login
- ✅ **Blog Management**: Create, read, update, and delete blog posts
- ✅ **Comment System**: User-associated comments with threaded discussions
- ✅ **Cross-Platform**: Web and mobile applications with shared API
- ✅ **Modern Stack**: FastAPI + SQLAlchemy + Next.js + Flutter
- ✅ **Admin Panel**: SQLAdmin interface at `/admin`
- ✅ **Type Safety**: OpenAPI client generation for web and mobile
- ✅ **Testing**: Comprehensive test coverage with pytest, Vitest, and Flutter tests
- ✅ **CI/CD**: GitHub Actions workflows for automated testing and deployment

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/napestershine/BloggingApp.git
   cd BloggingApp
   ```

2. **Start with Docker** (recommended):
   ```bash
   cd infra/docker
   docker-compose up --build
   ```

3. **Access the applications**:
   - Web: http://localhost:3000
   - API: http://localhost:8000/docs
   - Admin: http://localhost:8000/admin

## Technology Stack

### Backend (API)
- **FastAPI** with Pydantic v2 for API development
- **SQLAlchemy** with async support for database operations
- **Alembic** for database migrations
- **PostgreSQL 16** for production database
- **JWT** for authentication
- **SQLAdmin** for admin interface
- **pytest + httpx** for testing (≥85% coverage)

### Frontend (Web)
- **Next.js** with TypeScript for server-side rendering
- **Tailwind CSS** for styling
- **openapi-typescript** for type-safe API client generation
- **Vitest + React Testing Library** for unit testing
- **Playwright** for end-to-end testing

### Mobile
- **Flutter** with Material Design 3
- **dio** for HTTP client with API integration
- **flutter_test + integration_test** for comprehensive testing
- State management with Provider pattern

### Infrastructure
- **Docker** with multi-stage builds
- **PostgreSQL 16** with health checks
- **GitHub Actions** for CI/CD
- **MkDocs Material** for documentation

## Getting Started

Ready to dive in? Check out our [Quick Start Guide](getting-started/quick-start.md) to get the application running locally in minutes.

For detailed setup instructions, see the [Installation Guide](getting-started/installation.md).

## Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details on how to get started.

## License

This project is open source. Please check individual components for specific licensing information.