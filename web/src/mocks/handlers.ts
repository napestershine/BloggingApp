import { http, HttpResponse } from 'msw'

// Mock API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export const handlers = [
  // Mock posts endpoint
  http.get(`${API_BASE_URL}/posts`, () => {
    return HttpResponse.json({
      posts: [
        {
          id: 1,
          title: 'First Blog Post',
          content: 'This is the content of the first blog post.',
          author_username: 'testuser',
          published: '2024-01-01T00:00:00Z',
          slug: 'first-blog-post',
          total_comments: 3,
          views: 150
        },
        {
          id: 2,
          title: 'Second Blog Post', 
          content: 'This is the content of the second blog post.',
          author_username: 'author2',
          published: '2024-01-02T00:00:00Z',
          slug: 'second-blog-post',
          total_comments: 1,
          views: 85
        }
      ],
      total: 2,
      has_more: false,
      offset: 0
    })
  }),

  // Mock single post endpoint
  http.get(`${API_BASE_URL}/posts/:slug`, ({ params }) => {
    const { slug } = params
    return HttpResponse.json({
      id: 1,
      title: 'First Blog Post',
      content: 'This is the content of the first blog post.',
      author_username: 'testuser',
      published: '2024-01-01T00:00:00Z',
      slug: slug as string,
      total_comments: 3,
      views: 150
    })
  }),

  // Mock search posts endpoint
  http.get(`${API_BASE_URL}/posts/search`, ({ request }) => {
    const url = new URL(request.url)
    const query = url.searchParams.get('q')
    
    if (!query) {
      return HttpResponse.json({
        results: [],
        total: 0,
        has_more: false,
        offset: 0
      })
    }

    return HttpResponse.json({
      results: [
        {
          id: 1,
          title: 'Search Result Post',
          content: `This post matches the search term: ${query}`,
          author_username: 'testuser',
          published: '2024-01-01T00:00:00Z',
          slug: 'search-result-post'
        }
      ],
      total: 1,
      has_more: false,
      offset: 0
    })
  }),

  // Mock auth endpoints
  http.post(`${API_BASE_URL}/auth/login`, async ({ request }) => {
    const { username, password } = await request.json() as { username: string; password: string }
    
    if (username === 'testuser' && password === 'password') {
      return HttpResponse.json({
        access_token: 'mock-jwt-token',
        token_type: 'bearer',
        user: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com'
        }
      })
    }
    
    return HttpResponse.json(
      { detail: 'Incorrect username or password' },
      { status: 401 }
    )
  }),

  http.post(`${API_BASE_URL}/auth/register`, async ({ request }) => {
    const { username, email, password } = await request.json() as { 
      username: string; 
      email: string; 
      password: string 
    }
    
    return HttpResponse.json({
      access_token: 'mock-jwt-token',
      token_type: 'bearer',
      user: {
        id: 2,
        username,
        email
      }
    })
  }),

  // Mock user profile endpoint
  http.get(`${API_BASE_URL}/users/me`, ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return HttpResponse.json(
        { detail: 'Not authenticated' },
        { status: 401 }
      )
    }
    
    return HttpResponse.json({
      id: 1,
      username: 'testuser',
      email: 'test@example.com'
    })
  }),

  // Mock comments endpoint
  http.get(`${API_BASE_URL}/posts/:postId/comments`, () => {
    return HttpResponse.json({
      comments: [
        {
          id: 1,
          content: 'Great post!',
          author_username: 'commenter1',
          created_at: '2024-01-01T12:00:00Z'
        }
      ],
      total: 1
    })
  }),

  // Mock error scenario for testing error handling
  http.get(`${API_BASE_URL}/posts/error`, () => {
    return HttpResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    )
  }),
]