# Next.js Implementation Guide for BloggingApp Web Platform

This guide provides practical steps to implement a Next.js web platform for the BloggingApp, leveraging the existing FastAPI backend.

## Quick Start Setup

### Prerequisites
- Node.js 18+ and npm/yarn
- Existing FastAPI backend running (see [python/README.md](../python/README.md))
- Basic knowledge of React/TypeScript

### 1. Initialize Next.js Project

```bash
# Create new Next.js project in the root directory
npx create-next-app@latest blog-web --typescript --tailwind --eslint --app
cd blog-web

# Install additional dependencies for blogging features
npm install @next/mdx @mdx-js/loader @mdx-js/react
npm install next-auth @auth/prisma-adapter
npm install swr axios
npm install @headlessui/react @heroicons/react
npm install next-seo
npm install gray-matter remark remark-html
```

### 2. Project Structure

```
blog-web/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx
│   ├── blog/
│   │   ├── page.tsx              # Blog listing
│   │   └── [slug]/
│   │       └── page.tsx          # Blog post detail
│   ├── auth/
│   │   ├── login/
│   │   └── register/
│   └── api/
│       ├── auth/
│       └── proxy/                # Proxy to FastAPI
├── components/
│   ├── BlogCard.tsx
│   ├── BlogPost.tsx
│   ├── Navigation.tsx
│   └── SEO/
│       └── MetaTags.tsx
├── lib/
│   ├── api.ts                    # FastAPI integration
│   ├── auth.ts                   # NextAuth configuration
│   └── types.ts                  # Shared TypeScript types
├── public/
└── styles/
```

### 3. FastAPI Integration

Create a client library to interact with the existing FastAPI backend:

```typescript
// lib/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface BlogPost {
  id: number;
  title: string;
  content: string;
  author: string;
  created_at: string;
  updated_at: string;
  slug?: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
}

export const blogAPI = {
  // Get all blog posts
  getPosts: async (): Promise<BlogPost[]> => {
    const response = await apiClient.get('/posts');
    return response.data;
  },

  // Get single blog post
  getPost: async (id: number): Promise<BlogPost> => {
    const response = await apiClient.get(`/posts/${id}`);
    return response.data;
  },

  // Create new blog post
  createPost: async (post: Partial<BlogPost>): Promise<BlogPost> => {
    const response = await apiClient.post('/posts', post);
    return response.data;
  },

  // User authentication
  login: async (credentials: { username: string; password: string }) => {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  },

  register: async (userData: { username: string; email: string; password: string }) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },
};
```

### 4. SEO-Optimized Blog Pages

```typescript
// app/blog/[slug]/page.tsx
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { blogAPI } from '@/lib/api';
import BlogPost from '@/components/BlogPost';

interface BlogPageProps {
  params: { slug: string };
}

// Generate static params for build-time optimization
export async function generateStaticParams() {
  const posts = await blogAPI.getPosts();
  return posts.map((post) => ({
    slug: post.slug || post.id.toString(),
  }));
}

// Generate metadata for SEO
export async function generateMetadata({ params }: BlogPageProps): Promise<Metadata> {
  try {
    const post = await blogAPI.getPost(parseInt(params.slug));
    
    return {
      title: post.title,
      description: post.content.substring(0, 160) + '...',
      openGraph: {
        title: post.title,
        description: post.content.substring(0, 160) + '...',
        type: 'article',
        publishedTime: post.created_at,
        modifiedTime: post.updated_at,
        authors: [post.author],
      },
      twitter: {
        card: 'summary_large_image',
        title: post.title,
        description: post.content.substring(0, 160) + '...',
      },
    };
  } catch {
    return {
      title: 'Post Not Found',
    };
  }
}

export default async function BlogPage({ params }: BlogPageProps) {
  try {
    const post = await blogAPI.getPost(parseInt(params.slug));
    
    return (
      <main className="container mx-auto px-4 py-8">
        <BlogPost post={post} />
      </main>
    );
  } catch {
    notFound();
  }
}
```

### 5. Blog Listing with ISR

```typescript
// app/blog/page.tsx
import { Metadata } from 'next';
import { blogAPI } from '@/lib/api';
import BlogCard from '@/components/BlogCard';

export const metadata: Metadata = {
  title: 'Blog Posts | BloggingApp',
  description: 'Discover amazing blog posts on our platform',
};

// Enable Incremental Static Regeneration
export const revalidate = 60; // Revalidate every 60 seconds

export default async function BlogListPage() {
  const posts = await blogAPI.getPosts();

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Latest Blog Posts</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map((post) => (
          <BlogCard key={post.id} post={post} />
        ))}
      </div>
    </main>
  );
}
```

### 6. Authentication Integration

```typescript
// lib/auth.ts
import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import { blogAPI } from './api';

export const authOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        username: { label: 'Username', type: 'text' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.username || !credentials?.password) {
          return null;
        }

        try {
          const response = await blogAPI.login({
            username: credentials.username,
            password: credentials.password,
          });

          if (response.access_token) {
            return {
              id: response.user.id,
              name: response.user.username,
              email: response.user.email,
              accessToken: response.access_token,
            };
          }
        } catch (error) {
          console.error('Authentication failed:', error);
        }

        return null;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.accessToken;
      }
      return token;
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken;
      return session;
    },
  },
  pages: {
    signIn: '/auth/login',
  },
};

export default NextAuth(authOptions);
```

### 7. Environment Configuration

```bash
# .env.local
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 8. Deployment Configuration

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost', 'your-api-domain.com'],
  },
  async rewrites() {
    return [
      {
        source: '/api/proxy/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
```

## Development Workflow

### 1. Start Development Servers

```bash
# Terminal 1: Start FastAPI backend
cd python
docker-compose up

# Terminal 2: Start Next.js development server
cd blog-web
npm run dev
```

### 2. Build and Deploy

```bash
# Build for production
npm run build

# Start production server
npm start

# Deploy to Vercel (recommended)
npx vercel --prod
```

## Integration with Existing Features

### Mobile App API Compatibility
The Next.js web app can use the same FastAPI endpoints as the Flutter mobile app, ensuring consistency:

- Authentication endpoints: `/auth/login`, `/auth/register`
- Blog post CRUD: `/posts`, `/posts/{id}`
- User management: `/users/me`, `/users/profile`
- Comments: `/posts/{id}/comments`

### Shared Data Models
Create TypeScript interfaces that match the existing Python Pydantic models to ensure type safety across platforms.

### Progressive Enhancement
1. **Phase 1**: Static blog listing and reading
2. **Phase 2**: User authentication and basic interactions
3. **Phase 3**: Full CRUD operations and advanced features
4. **Phase 4**: Real-time features and PWA capabilities

## SEO Implementation Checklist

- ✅ Server-side rendering for all blog pages
- ✅ Dynamic meta tags for each blog post
- ✅ OpenGraph and Twitter Card support
- ✅ Structured data (JSON-LD) for blog posts
- ✅ Sitemap generation (`/sitemap.xml`)
- ✅ RSS feed support (`/rss.xml`)
- ✅ Clean, SEO-friendly URLs
- ✅ Performance optimization (Core Web Vitals)

This implementation provides a solid foundation for a high-performance, SEO-optimized web platform that integrates seamlessly with your existing FastAPI backend while maintaining the mobile Flutter app for native mobile experiences.