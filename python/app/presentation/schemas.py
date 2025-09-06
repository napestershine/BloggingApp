"""Presentation layer schemas for request/response DTOs"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.domain.entities import UserRole, PostStatus


# User schemas
class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)
    retyped_password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    name: str
    role: UserRole
    created_at: Optional[datetime] = None
    email_verified: bool = False
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class LoginRequest(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Post schemas
class PostCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    status: PostStatus = PostStatus.DRAFT


class PostUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    status: Optional[PostStatus] = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    slug: str
    author_id: int
    status: PostStatus
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    view_count: int = 0
    featured: bool = False


class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total: int
    skip: int
    limit: int


# Generic response schemas
class SuccessResponse(BaseModel):
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None