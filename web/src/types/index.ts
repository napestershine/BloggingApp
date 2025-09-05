// TypeScript interfaces matching the FastAPI backend models

export enum UserRole {
  USER = "user",
  ADMIN = "admin",
  SUPER_ADMIN = "super_admin"
}

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
  name: string;
  role: UserRole;
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

// Admin-specific types
export interface AdminStats {
  total_users: number;
  total_posts: number;
  total_comments: number;
  admin_users: number;
  new_users_today: number;
  new_posts_today: number;
  new_comments_today: number;
}

export interface UserManagementResponse {
  id: number;
  username: string;
  email: string;
  name: string;
  role: UserRole;
  created_at: string;
  email_verified: boolean;
  total_posts: number;
  total_comments: number;
}

export interface PostModerationResponse {
  id: number;
  title: string;
  content: string;
  slug?: string;
  published: string;
  author_id: number;
  author_username: string;
  author_name: string;
  total_comments: number;
  status?: string;
}

export interface CommentModerationResponse {
  id: number;
  content: string;
  published: string;
  author_id: number;
  author_username: string;
  author_name: string;
  blog_post_id: number;
  blog_post_title: string;
  status?: string;
}