# BloggingApp Web Platform

A modern Next.js web application for the BloggingApp platform, built with TypeScript, Tailwind CSS, and Docker support.

## Features

- **Modern Tech Stack**: Built with Next.js 15, React 19, TypeScript, and Tailwind CSS
- **SEO Optimized**: Server-side rendering for excellent search engine optimization
- **Responsive Design**: Mobile-first approach with beautiful UI components
- **Authentication**: Complete auth flow with JWT token management
- **API Integration**: Seamless integration with FastAPI backend
- **Docker Ready**: Complete containerization with docker-compose support
- **Production Ready**: Nginx reverse proxy configuration included

## Getting Started

### Prerequisites

- Node.js 20 or later
- npm or yarn
- Docker (optional, for containerized deployment)

### Development Setup

1. **Clean install dependencies:**
   ```bash
   # Remove existing node_modules and package-lock.json if upgrading
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   ```
   
   Update the environment variables:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_SITE_URL=http://localhost:3000
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Building for Production

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Start the production server:**
   ```bash
   npm start
   ```

## Docker Deployment

### Using Docker Compose (Recommended)

The easiest way to deploy the entire stack:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This will start:
- Next.js web app on port 3000
- FastAPI backend on port 8000
- Nginx reverse proxy on port 80/443 (with production profile)

### Using Docker Only

```bash
# Build the image
docker build -t blogging-app-web .

# Run the container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  blogging-app-web
```

### Production with Nginx

For production deployment with SSL:

```bash
# Start with nginx reverse proxy
docker-compose --profile production up -d
```

Make sure to:
1. Place SSL certificates in `./ssl/` directory
2. Update `nginx.conf` with your domain name
3. Configure environment variables for production

## Project Structure

```
web/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── api/            # API routes
│   │   ├── auth/           # Authentication pages
│   │   ├── blog/           # Blog pages
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Homepage
│   ├── components/         # React components
│   │   ├── AuthProvider.tsx
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── lib/               # Utility libraries
│   │   └── api.ts         # API client
│   ├── types/             # TypeScript type definitions
│   ├── utils/             # Helper functions
│   └── styles/            # Global styles
├── public/                # Static assets
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Multi-service setup
├── nginx.conf            # Nginx configuration
└── package.json          # Dependencies and scripts
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | FastAPI backend URL | `http://localhost:8000` |
| `NEXT_PUBLIC_SITE_URL` | Web app URL | `http://localhost:3000` |
| `NODE_ENV` | Environment mode | `development` |

## API Integration

The web app integrates with the FastAPI backend through:

- **Authentication**: Login, register, profile management
- **Blog Posts**: CRUD operations, pagination, search
- **Comments**: Add, view, and manage comments
- **Real-time Features**: WebSocket support for live updates

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler check
- `npm run test` - Run unit tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage report
- `npm run test:e2e` - Run end-to-end tests with Playwright
- `npm run test:e2e:ui` - Run E2E tests with Playwright UI

## Testing

This project includes a comprehensive testing setup with multiple testing layers:

### Unit & Integration Tests
- **Framework**: Vitest with React Testing Library
- **API Mocking**: MSW (Mock Service Worker) for API interception
- **Coverage**: V8 coverage provider
- **Setup**: Automated test environment with jsdom

```bash
# Run all unit tests
npm run test

# Run tests in watch mode during development
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### End-to-End Tests
- **Framework**: Playwright for cross-browser testing
- **Coverage**: User journey testing from browser perspective
- **Browsers**: Chromium, Firefox, and WebKit

```bash
# Run E2E tests
npm run test:e2e

# Run with interactive UI
npm run test:e2e:ui

# Install Playwright browsers (first time only)
npx playwright install
```

### Test Structure
```
src/
├── test/                    # Unit & integration tests
│   ├── setup.ts            # Test configuration
│   ├── *.test.tsx          # Component tests
│   └── *Integration.test.tsx # Integration tests
├── mocks/                   # MSW API mocks
│   ├── handlers.ts         # Mock API handlers
│   └── index.ts           # Mock exports
└── e2e/                    # Playwright E2E tests
    └── *.spec.ts          # E2E test files
```

### Test Coverage
The test suite covers:
- ✅ Component rendering and interaction
- ✅ API integration with mocked responses
- ✅ User authentication flows
- ✅ Search functionality
- ✅ Error handling scenarios
- ✅ Cross-browser compatibility (E2E)

### Continuous Integration
Tests run automatically on:
- Pull requests to main branch
- Pushes to main branch
- Changes in web directory or workflows

Coverage reports are uploaded to Codecov for tracking.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.