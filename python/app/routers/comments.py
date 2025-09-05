from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.models import Comment, User, BlogPost
from app.schemas.schemas import (
    Comment as CommentSchema, 
    CommentCreate, 
    CommentUpdate
)
from app.auth.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/", response_model=List[CommentSchema])
def get_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = db.query(Comment).offset(skip).limit(limit).all()
    return comments

@router.post("/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Check if blog post exists
    blog_post = db.query(BlogPost).filter(BlogPost.id == comment.blog_post_id).first()
    if not blog_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    
    db_comment = Comment(
        content=comment.content,
        blog_post_id=comment.blog_post_id,
        author_id=current_user.id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return db_comment

@router.get("/{comment_id}", response_model=CommentSchema)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Only author can update their comment
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment"
        )
    
    # Update content if provided
    if comment_update.content is not None:
        comment.content = comment_update.content
    
    db.commit()
    db.refresh(comment)
    return comment

@router.get("/blog_post/{blog_post_id}", response_model=List[CommentSchema])
def get_comments_for_blog_post(blog_post_id: int, db: Session = Depends(get_db)):
    # Check if blog post exists
    blog_post = db.query(BlogPost).filter(BlogPost.id == blog_post_id).first()
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    comments = db.query(Comment).filter(Comment.blog_post_id == blog_post_id).all()
    return comments