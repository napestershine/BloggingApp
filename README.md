# BloggingApp

A modern, full-stack blogging platform featuring a Flutter mobile application, Next.js web application, and a FastAPI backend. This project provides a complete solution for creating, managing, and publishing blog content with user authentication, comments, and social features across mobile and web platforms.

[![Dependabot Updates](https://github.com/napestershine/BloggingApp/actions/workflows/dependabot/dependabot-updates/badge.svg?branch=main)](https://github.com/napestershine/BloggingApp/actions/workflows/dependabot/dependabot-updates)

## 🏗️ Architecture

This project follows a **monorepo structure** with clearly separated applications and infrastructure:

```
BloggingApp/
├── apps/
│   ├── api/              # FastAPI backend with JWT auth & SQLAlchemy
│   ├── web/              # Next.js TypeScript frontend with SSR
│   └── mobile/           # Flutter mobile app with Material Design 3
├── infra/
│   └── docker/           # Docker configurations for all environments
├── docs/                 # MkDocs Material documentation
└── .github/workflows/    # CI/CD pipelines
```

### Key Technologies
- **Backend**: FastAPI + Pydantic v2 + SQLAlchemy (async) + Alembic + PostgreSQL 16
- **Web Frontend**: Next.js + TypeScript + Tailwind CSS + openapi-typescript
- **Mobile**: Flutter + dio HTTP client + Material Design 3
- **Infrastructure**: Docker + PostgreSQL 16 + GitHub Actions CI
- **Quality**: pytest+httpx (≥85% cov) + Vitest/RTL + Playwright + flutter_test
- **Admin**: SQLAdmin at `/admin` endpoint
- **Docs**: MkDocs Material with automated deployment

## 🚀 Quick Start

### Prerequisites

- **Flutter**: SDK 3.0.0+ with Dart (for mobile app)
- **Node.js**: 18+ with npm/yarn (for web app)
- **Python**: 3.12+ for the API backend
- **Docker**: (Optional) For containerized deployment

### Option 1: Docker Setup (Recommended for Testing)

1. Clone the repository:
   ```bash
   git clone https://github.com/napestershine/BloggingApp.git
   cd BloggingApp
   ```

2. **Frontend Only (Web)**: Test the Next.js app in isolation:
   ```bash
   docker compose -f docker-compose.web-only.yml up
   # Access at http://localhost:3000
   ```

2. **Full Stack** with PostgreSQL 16:
   ```bash
   cd infra/docker
   docker-compose up --build
   # Web: http://localhost:3000
   # API: http://localhost:8000/docs
   # Admin: http://localhost:8000/admin
   ```

3. **Development Mode** with hot reloading:
   ```bash
   cd infra/docker
   docker-compose -f docker-compose.dev.yml up
   ```

### Option 2: Legacy Docker Setup (Python Backend Only)

1. Start the backend API:
   ```bash
   cd python
   docker-compose up --build
   ```

2. Run the Flutter app (mobile):
   ```bash
   cd app
   flutter pub get
   flutter run
   ```

3. Run the Next.js web app:
   ```bash
   cd web
   npm install --legacy-peer-deps
   npm run dev
   ```

### Option 3: Manual Setup

1. **Set up the API backend**:
   ```bash
   cd python
   pip install -r requirements.txt
   cp .env.example .env  # Configure your settings
   uvicorn app.main:app --reload
   ```

2. **Set up the Flutter app** (mobile):
   ```bash
   cd app
   flutter pub get
   flutter run
   ```

3. **Set up the Next.js web app**:
   ```bash
   cd web
   npm install --legacy-peer-deps
   npm run dev
   ```

## 📱 Components

### [Flutter Mobile App](./apps/mobile/README.md)
- Modern Material Design 3 interface with responsive layouts
- User authentication with JWT tokens and secure storage
- Blog post creation, editing, and management
- Comments and social interactions with real-time updates
- dio HTTP client with type-safe API integration
- Comprehensive testing with flutter_test and integration_test
- Cross-platform support for iOS and Android

### [Next.js Web App](./apps/web/README.md)
- Modern web platform with TypeScript and Tailwind CSS
- Server-side rendering for excellent SEO performance
- openapi-typescript for type-safe API client generation
- Responsive design with mobile-first approach
- Complete authentication flow with JWT integration
- Testing with Vitest, React Testing Library, and Playwright
- Docker-ready with optimized production builds

### [FastAPI Backend](./apps/api/README.md)
- RESTful API with automatic OpenAPI documentation at `/openapi.json`
- JWT-based authentication and authorization
- Async SQLAlchemy ORM with PostgreSQL 16 and Alembic migrations
- User, blog post, and comment management with full CRUD operations
- SQLAdmin interface at `/admin` for easy administration
- Comprehensive test suite with pytest+httpx (≥85% coverage)
- CORS support for cross-origin requests

### [Development Tasks](./tasks/README.md)
- Comprehensive roadmap with 50+ planned features
- Organized by priority and category
- Social features, SEO, analytics, and monetization
- Performance optimization and security enhancements

## 📚 API Documentation

Once the FastAPI backend is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Key Features

### Current Features
- ✅ User registration and authentication
- ✅ JWT token-based security
- ✅ Create, read, and manage blog posts
- ✅ Comment system with user associations
- ✅ RESTful API with OpenAPI documentation
- ✅ Flutter mobile app with state management
- ✅ Next.js web app with SSR and TypeScript
- ✅ Responsive Material Design UI (mobile) and Tailwind CSS (web)

### Planned Features (See [Tasks](./tasks/README.md))
- 🔄 Rich text editor for blog posts
- 🔄 Image upload and media management
- 🔄 Social features (likes, shares, follows)
- 🔄 SEO optimization and content discovery
- 🔄 Analytics and insights dashboard
- 🔄 Performance optimizations
- 🔄 Monetization features

## 🛠️ Development

### Project Structure
```
BloggingApp/
├── app/                    # Flutter mobile application
│   ├── lib/               # Dart source code
│   ├── android/           # Android-specific files
│   ├── ios/               # iOS-specific files
│   └── README.md          # Flutter app documentation
├── web/                    # Next.js web application
│   ├── src/               # TypeScript source code
│   ├── public/            # Static assets
│   ├── Dockerfile         # Container configuration
│   └── README.md          # Web app documentation
├── python/                # FastAPI backend
│   ├── app/               # Python source code
│   ├── Dockerfile         # Container configuration
│   └── README.md          # API documentation
├── tasks/                 # Development roadmap
│   ├── 01-user-experience/
│   ├── 02-content-management/
│   └── ...                # Task categories
└── README.md              # This file
```

### Running Tests

**Flutter App**:
```bash
cd app
flutter test
```

**Next.js Web App**:
```bash
cd web
npm run test # (if tests are configured)
npm run lint
npm run type-check
```

**FastAPI Backend**:
```bash
cd python
pytest

# For PostgreSQL testing (CI environment)
TEST_DATABASE_URL=postgresql://user:password@host:port/db pytest
```

### Code Quality

**Flutter**:
```bash
flutter analyze
flutter test
```

**Next.js Web App**:
```bash
npm run lint
npm run type-check
```

**Python**:
```bash
black app/
isort app/
mypy app/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read the component-specific READMEs for detailed setup and contribution guidelines:
- [Flutter App Contributing](./app/README.md#contributing)
- [Next.js Web App Development](./web/README.md#contributing)
- [API Backend Development](./python/README.md#development)

## 📄 License

This project is open source. Please check individual components for specific licensing information.

## 🌐 Web Platform Analysis

We've conducted a comprehensive analysis of web platform options:

- **[Web Technology Comparison](./docs/WEB_TECHNOLOGY_COMPARISON.md)** - Detailed comparison of Flutter Web vs Next.js vs Nuxt.js
- **[Executive Summary](./docs/EXECUTIVE_SUMMARY.md)** - Quick overview and recommendations  
- **[Next.js Implementation Guide](./docs/NEXTJS_IMPLEMENTATION_GUIDE.md)** - Step-by-step implementation roadmap
- **[Next.js Demo](./examples/nextjs-demo/)** - Working example with FastAPI integration

**Key Finding**: Next.js is recommended for the web platform due to superior SEO capabilities and performance optimization for content-driven applications.

## 🔗 Links

- [Flutter App Documentation](./app/README.md)
- [Next.js Web App Documentation](./web/README.md)
- [FastAPI Backend Documentation](./python/README.md)
- [Development Tasks & Roadmap](./tasks/README.md)
- [API Documentation](http://localhost:8000/docs) (when running)
- [Web Platform Analysis](./docs/WEB_TECHNOLOGY_COMPARISON.md)

---

**Getting Started**: Begin with the [Quick Start](#-quick-start) section above, then explore the component-specific documentation for detailed setup instructions.
