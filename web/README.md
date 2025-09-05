# BloggingApp Web Platform

A modern Next.js web application for the BloggingApp platform, built with TypeScript, Tailwind CSS, and Docker support.

## Features

- **Modern Tech Stack**: Built with Next.js 14, TypeScript, and Tailwind CSS
- **SEO Optimized**: Server-side rendering for excellent search engine optimization
- **Responsive Design**: Mobile-first approach with beautiful UI components
- **Authentication**: Complete auth flow with JWT token management
- **API Integration**: Seamless integration with FastAPI backend
- **Docker Ready**: Complete containerization with docker-compose support
- **Production Ready**: Nginx reverse proxy configuration included

## Getting Started

### Prerequisites

- Node.js 18 or later
- npm or yarn
- Docker (optional, for containerized deployment)

### Development Setup

1. **Install dependencies:**
   ```bash
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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.