import axios from 'axios';
import { BlogPost, User, AuthResponse, Comment, PaginatedResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);

// Blog Post API functions
export const blogAPI = {
  // Get all blog posts with pagination
  getPosts: async (page = 1, size = 10): Promise<PaginatedResponse<BlogPost>> => {
    const response = await apiClient.get(`/posts?page=${page}&size=${size}`);
    return response.data;
  },

  // Get single blog post by ID
  getPost: async (id: number): Promise<BlogPost> => {
    const response = await apiClient.get(`/posts/${id}`);
    return response.data;
  },

  // Get blog post by slug
  getPostBySlug: async (slug: string): Promise<BlogPost> => {
    const response = await apiClient.get(`/posts/slug/${slug}`);
    return response.data;
  },

  // Create new blog post (requires authentication)
  createPost: async (post: Omit<BlogPost, 'id' | 'created_at' | 'updated_at'>): Promise<BlogPost> => {
    const response = await apiClient.post('/posts', post);
    return response.data;
  },

  // Update blog post (requires authentication)
  updatePost: async (id: number, post: Partial<BlogPost>): Promise<BlogPost> => {
    const response = await apiClient.put(`/posts/${id}`, post);
    return response.data;
  },

  // Delete blog post (requires authentication)
  deletePost: async (id: number): Promise<void> => {
    await apiClient.delete(`/posts/${id}`);
  },

  // Get comments for a blog post
  getComments: async (postId: number): Promise<Comment[]> => {
    const response = await apiClient.get(`/posts/${postId}/comments`);
    return response.data;
  },

  // Add comment to blog post (requires authentication)
  addComment: async (postId: number, content: string): Promise<Comment> => {
    const response = await apiClient.post(`/posts/${postId}/comments`, { content });
    return response.data;
  },

  // Search blog posts
  searchPosts: async (query: string, page = 1, size = 10): Promise<PaginatedResponse<BlogPost>> => {
    const response = await apiClient.get(`/posts/search?q=${encodeURIComponent(query)}&page=${page}&size=${size}`);
    return response.data;
  },
};

// Authentication API functions
export const authAPI = {
  // User login
  login: async (credentials: { username: string; password: string }): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  },

  // User registration
  register: async (userData: { 
    username: string; 
    email: string; 
    password: string; 
  }): Promise<User> => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  // Get current user profile (requires authentication)
  getProfile: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  // Update user profile (requires authentication)
  updateProfile: async (userData: Partial<User>): Promise<User> => {
    const response = await apiClient.put('/auth/me', userData);
    return response.data;
  },

  // Logout (optional backend call)
  logout: async (): Promise<void> => {
    try {
      await apiClient.post('/auth/logout');
    } catch (error) {
      // Handle logout error silently
    } finally {
      tokenUtils.removeToken();
    }
  },
};

// Utility functions for token management
export const tokenUtils = {
  setToken: (token: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  },

  getToken: (): string | null => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return null;
  },

  removeToken: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  },

  isAuthenticated: (): boolean => {
    return !!tokenUtils.getToken();
  },
};

export default apiClient;