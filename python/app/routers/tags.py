from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.models import Tag, User
from app.schemas.schemas import (
    Tag as TagSchema,
    TagCreate
)
from app.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/", response_model=List[TagSchema])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tags"""
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags

@router.post("/", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new tag"""
    
    # Normalize tag name (lowercase, strip whitespace)
    tag_name = tag.name.strip().lower()
    
    if not tag_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag name cannot be empty"
        )
    
    # Check if tag already exists
    existing_tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if existing_tag:
        # Return existing tag instead of error for better UX
        return existing_tag
    
    db_tag = Tag(
        name=tag_name,
        created_by=current_user.id
    )
    
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    
    logger.info(f"Tag created: {tag_name} by user {current_user.id}")
    return db_tag

@router.get("/{tag_id}", response_model=TagSchema)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """Get a specific tag by ID"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.get("/search/{tag_name}", response_model=List[TagSchema])
def search_tags(tag_name: str, db: Session = Depends(get_db)):
    """Search tags by name (for autocomplete)"""
    tags = db.query(Tag).filter(
        Tag.name.ilike(f"%{tag_name.lower()}%")
    ).limit(10).all()
    return tags

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a tag"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Only creator can delete their tag (or admin in future)
    if tag.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this tag"
        )
    
    db.delete(tag)
    db.commit()
    
    logger.info(f"Tag deleted: {tag.name} by user {current_user.id}")
    return