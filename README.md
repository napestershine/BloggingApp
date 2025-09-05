# BloggingApp

A modern, full-stack blogging platform featuring a Flutter mobile application, Next.js web application, and a FastAPI backend. This project provides a complete solution for creating, managing, and publishing blog content with user authentication, comments, and social features across mobile and web platforms.

## 🏗️ Architecture

- **Mobile Frontend**: Flutter mobile application with Material Design 3 UI
- **Web Frontend**: Next.js web application with TypeScript, Tailwind CSS, and SSR
- **Backend**: FastAPI-based REST API with JWT authentication
- **Database**: SQLAlchemy ORM with SQLite (dev) / PostgreSQL (prod) support
- **Authentication**: JWT token-based security
- **Documentation**: Auto-generated OpenAPI/Swagger docs

## 🚀 Quick Start

### Prerequisites

- **Flutter**: SDK 3.0.0+ with Dart (for mobile app)
- **Node.js**: 18+ with npm/yarn (for web app)
- **Python**: 3.12+ for the API backend
- **Docker**: (Optional) For containerized deployment

### Option 1: Docker Setup (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/napestershine/BloggingApp.git
   cd BloggingApp
   ```

2. Start the backend API:
   ```bash
   cd python
   docker-compose up --build
   ```

3. Run the Flutter app (mobile):
   ```bash
   cd app
   flutter pub get
   flutter run
   ```

4. Run the Next.js web app:
   ```bash
   cd web
   npm install
   npm run dev
   ```

### Option 2: Manual Setup

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
   npm install
   npm run dev
   ```

## 📱 Components

### [Flutter Mobile App](./app/README.md)
- Modern Material Design 3 interface
- User authentication with JWT tokens
- Blog post creation and management
- Comments and social interactions
- Responsive UI for different screen sizes

### [Next.js Web App](./web/README.md)
- Modern web platform with TypeScript and Tailwind CSS
- Server-side rendering for excellent SEO
- Responsive design with mobile-first approach
- Complete authentication flow and API integration
- Docker-ready with production configuration

### [FastAPI Backend](./python/README.md)
- RESTful API with automatic documentation
- JWT-based authentication and authorization
- SQLAlchemy ORM with database migrations
- User, blog post, and comment management
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