import axios from 'axios';
import { 
  BlogPost, 
  User, 
  AuthResponse, 
  Comment, 
  PaginatedResponse,
  SearchSuggestion,
  SearchFilters,
  UserFollowResponse,
  UserFollowStats,
  FollowerUser,
  NotificationModel,
  WhatsAppSettings,
  WhatsAppSettingsUpdate,
  BookmarkResponse,
  BookmarkStats
} from '@/types';

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

// Search API functions
export const searchAPI = {
  // Search posts with filters
  searchPosts: async (params: {
    q: string;
    category?: string;
    tag?: string;
    author?: string;
    skip?: number;
    limit?: number;
  }): Promise<BlogPost[]> => {
    const queryParams = new URLSearchParams();
    queryParams.append('q', params.q);
    if (params.category) queryParams.append('category', params.category);
    if (params.tag) queryParams.append('tag', params.tag);
    if (params.author) queryParams.append('author', params.author);
    if (params.skip) queryParams.append('skip', params.skip.toString());
    if (params.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await apiClient.get(`/search/?${queryParams.toString()}`);
    return response.data;
  },

  // Get search suggestions
  getSuggestions: async (q: string, limit = 5): Promise<SearchSuggestion[]> => {
    const response = await apiClient.get(`/search/suggestions?q=${encodeURIComponent(q)}&limit=${limit}`);
    return response.data;
  },

  // Get search filters
  getFilters: async (): Promise<SearchFilters> => {
    const response = await apiClient.get('/search/filters');
    return response.data;
  },
};

// User Follow API functions
export const followAPI = {
  // Follow a user
  followUser: async (userId: number): Promise<UserFollowResponse> => {
    const response = await apiClient.post(`/follow/users/${userId}`);
    return response.data;
  },

  // Unfollow a user
  unfollowUser: async (userId: number): Promise<UserFollowResponse> => {
    const response = await apiClient.delete(`/follow/users/${userId}`);
    return response.data;
  },

  // Get user's followers
  getFollowers: async (userId: number, skip = 0, limit = 20): Promise<FollowerUser[]> => {
    const response = await apiClient.get(`/follow/users/${userId}/followers?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Get users that a user is following
  getFollowing: async (userId: number, skip = 0, limit = 20): Promise<FollowerUser[]> => {
    const response = await apiClient.get(`/follow/users/${userId}/following?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Get follow statistics
  getStats: async (userId: number): Promise<UserFollowStats> => {
    const response = await apiClient.get(`/follow/users/${userId}/stats`);
    return response.data;
  },

  // Get current user's following
  getMyFollowing: async (skip = 0, limit = 20): Promise<FollowerUser[]> => {
    const response = await apiClient.get(`/follow/me/following?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Get current user's followers
  getMyFollowers: async (skip = 0, limit = 20): Promise<FollowerUser[]> => {
    const response = await apiClient.get(`/follow/me/followers?skip=${skip}&limit=${limit}`);
    return response.data;
  },
};

// Notification API functions
export const notificationAPI = {
  // Get notifications
  getNotifications: async (params?: {
    is_read?: boolean;
    skip?: number;
    limit?: number;
  }): Promise<NotificationModel[]> => {
    const queryParams = new URLSearchParams();
    if (params?.is_read !== undefined) queryParams.append('is_read', params.is_read.toString());
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await apiClient.get(`/notifications/?${queryParams.toString()}`);
    return response.data;
  },

  // Mark notification as read
  markAsRead: async (notificationId: number): Promise<void> => {
    await apiClient.patch(`/notifications/${notificationId}/read`);
  },

  // Mark all notifications as read
  markAllAsRead: async (): Promise<void> => {
    await apiClient.patch('/notifications/read-all');
  },

  // Get WhatsApp settings
  getWhatsAppSettings: async (): Promise<WhatsAppSettings> => {
    const response = await apiClient.get('/notifications/whatsapp');
    return response.data;
  },

  // Update WhatsApp settings
  updateWhatsAppSettings: async (settings: WhatsAppSettingsUpdate): Promise<WhatsAppSettings> => {
    const response = await apiClient.put('/notifications/whatsapp', settings);
    return response.data;
  },

  // Test WhatsApp notification
  testWhatsApp: async (): Promise<{ message: string }> => {
    const response = await apiClient.post('/notifications/whatsapp/test');
    return response.data;
  },
};

// Bookmark API functions
export const bookmarkAPI = {
  // Bookmark a post
  bookmarkPost: async (postId: number): Promise<BookmarkResponse> => {
    const response = await apiClient.post(`/bookmarks/posts/${postId}`);
    return response.data;
  },

  // Remove bookmark
  removeBookmark: async (postId: number): Promise<void> => {
    await apiClient.delete(`/bookmarks/posts/${postId}`);
  },

  // Get user's bookmarks
  getBookmarks: async (skip = 0, limit = 20): Promise<BlogPost[]> => {
    const response = await apiClient.get(`/bookmarks/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Get bookmark stats for a post
  getPostStats: async (postId: number): Promise<BookmarkStats> => {
    const response = await apiClient.get(`/bookmarks/posts/${postId}`);
    return response.data;
  },

  // Get user's bookmark stats
  getUserStats: async (): Promise<BookmarkStats> => {
    const response = await apiClient.get('/bookmarks/stats');
    return response.data;
  },

  // Get recent bookmarks
  getRecentBookmarks: async (limit = 5): Promise<BlogPost[]> => {
    const response = await apiClient.get(`/bookmarks/recent?limit=${limit}`);
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
    } catch {
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