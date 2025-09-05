from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.models import Category, User
from app.schemas.schemas import (
    Category as CategorySchema,
    CategoryCreate,
    CategoryUpdate
)
from app.auth.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/categories", tags=["categories"])

def create_slug(name: str) -> str:
    """Create a URL-friendly slug from a category name"""
    return name.lower().replace(" ", "-").replace("'", "").replace("&", "and")

@router.get("/", response_model=List[CategorySchema])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new category"""
    
    # Generate slug if not provided
    slug = category.slug
    if not slug:
        slug = create_slug(category.name)
    
    # Check if category name already exists
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    # Check if slug already exists
    existing_slug = db.query(Category).filter(Category.slug == slug).first()
    if existing_slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this slug already exists"
        )
    
    db_category = Category(
        name=category.name,
        description=category.description,
        slug=slug,
        created_by=current_user.id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    logger.info(f"Category created: {category.name} by user {current_user.id}")
    return db_category

@router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Only creator can update their category (or admin in future)
    if category.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this category"
        )
    
    # Update fields if provided
    if category_update.name is not None:
        # Check if new name already exists
        existing_category = db.query(Category).filter(
            Category.name == category_update.name,
            Category.id != category_id
        ).first()
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        category.name = category_update.name
        
        # Update slug if name changed and no custom slug provided
        if category_update.slug is None:
            new_slug = create_slug(category_update.name)
            existing_slug = db.query(Category).filter(
                Category.slug == new_slug,
                Category.id != category_id
            ).first()
            if not existing_slug:
                category.slug = new_slug
    
    if category_update.description is not None:
        category.description = category_update.description
    
    if category_update.slug is not None:
        # Check if new slug already exists
        existing_slug = db.query(Category).filter(
            Category.slug == category_update.slug,
            Category.id != category_id
        ).first()
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this slug already exists"
            )
        category.slug = category_update.slug
    
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Only creator can delete their category (or admin in future)
    if category.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this category"
        )
    
    db.delete(category)
    db.commit()
    
    logger.info(f"Category deleted: {category.name} by user {current_user.id}")
    return