// TypeScript interfaces matching the FastAPI backend models
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
  created_at: string;
}

export interface Comment {
  id: number;
  content: string;
  author: string;
  post_id: number;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Search interfaces
export interface SearchSuggestion {
  text: string;
  type: string;
  description: string;
}

export interface SearchFilters {
  categories: CategoryFilter[];
  tags: TagFilter[];
  authors: AuthorFilter[];
}

export interface CategoryFilter {
  name: string;
  slug: string;
}

export interface TagFilter {
  name: string;
  post_count: number;
}

export interface AuthorFilter {
  username: string;
  post_count: number;
}

// User follow interfaces
export interface UserFollowResponse {
  following_id: number;
  follower_id: number;
  is_following: boolean;
  created_at: string | null;
}

export interface UserFollowStats {
  followers_count: number;
  following_count: number;
  is_following: boolean | null;
}

export interface FollowerUser {
  id: number;
  username: string;
  name: string;
  email?: string;
}

// Notification interfaces
export interface NotificationModel {
  id: number;
  user_id: number;
  type: string;
  message: string;
  is_read: boolean;
  created_at: string;
  post_id?: number;
  from_user_id?: number;
  from_user_name?: string;
}

export interface WhatsAppSettings {
  whatsapp_number?: string;
  whatsapp_notifications_enabled: boolean;
  notify_on_new_posts: boolean;
  notify_on_comments: boolean;
  notify_on_mentions: boolean;
}

export interface WhatsAppSettingsUpdate {
  whatsapp_number?: string;
  whatsapp_notifications_enabled?: boolean;
  notify_on_new_posts?: boolean;
  notify_on_comments?: boolean;
  notify_on_mentions?: boolean;
}

// Bookmark interfaces
export interface BookmarkResponse {
  id: number;
  user_id: number;
  post_id: number;
  created_at: string;
  post?: BookmarkPost;
}

export interface BookmarkPost {
  id: number;
  title: string;
  slug: string;
  author: string;
}

export interface BookmarkStats {
  total_bookmarks: number;
  is_bookmarked?: boolean;
}