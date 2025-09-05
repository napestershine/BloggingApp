from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.models import BlogPost, User
from app.schemas.schemas import (
    BlogPost as BlogPostSchema, 
    BlogPostCreate, 
    BlogPostUpdate
)
from app.auth.auth import get_current_user
from app.services.notification_service import whatsapp_service
import asyncio
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/blog_posts", tags=["blog_posts"])

@router.get("/", response_model=List[BlogPostSchema])
def get_blog_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(BlogPost).offset(skip).limit(limit).all()
    return posts

@router.post("/", response_model=BlogPostSchema, status_code=status.HTTP_201_CREATED)
async def create_blog_post(
    post: BlogPostCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Generate slug if not provided
    slug = post.slug
    if not slug:
        slug = post.title.lower().replace(" ", "-").replace("'", "")
    
    # Check if slug already exists
    existing_post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if existing_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    
    db_post = BlogPost(
        title=post.title,
        content=post.content,
        slug=slug,
        author_id=current_user.id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Send WhatsApp notifications to followers (for now, we'll skip this as we don't have a follower system yet)
    # In the future, this would notify users who follow this author
    try:
        # For demonstration, we could notify the author themselves about their post
        if (current_user.whatsapp_notifications_enabled and 
            current_user.whatsapp_number and 
            current_user.notify_on_new_posts):
            
            asyncio.create_task(
                whatsapp_service.notify_new_blog_post(
                    current_user.name,
                    post.title,
                    current_user.whatsapp_number
                )
            )
    except Exception as e:
        # Don't fail the post creation if notification fails
        logger.error(f"Failed to send WhatsApp notification for new post: {e}")
    
    return db_post

@router.get("/{post_id}", response_model=BlogPostSchema)
def get_blog_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post

@router.put("/{post_id}", response_model=BlogPostSchema)
def update_blog_post(
    post_id: int,
    post_update: BlogPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Only author can update their post
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )
    
    # Update fields if provided
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    if post_update.slug is not None:
        # Check if new slug already exists
        existing_post = db.query(BlogPost).filter(
            BlogPost.slug == post_update.slug,
            BlogPost.id != post_id
        ).first()
        if existing_post:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slug already exists"
            )
        post.slug = post_update.slug
    
    db.commit()
    db.refresh(post)
    return post
    
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Only author can delete their post
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    
    db.delete(post)
    db.commit()
    return