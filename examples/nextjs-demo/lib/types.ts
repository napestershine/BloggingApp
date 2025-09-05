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