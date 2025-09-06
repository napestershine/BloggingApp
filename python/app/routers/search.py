from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from app.database.connection import get_db
from app.models.models import BlogPost, User, Tag, Category, PostStatus
from app.schemas.schemas import (
    BlogPost as BlogPostSchema,
    SearchResult,
    SearchSuggestion
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/", response_model=List[BlogPostSchema])
def search_posts(
    q: str = Query(..., min_length=1, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    author: Optional[str] = Query(None, description="Filter by author username"),
    skip: int = Query(0, ge=0, description="Number of posts to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of posts to return"),
    db: Session = Depends(get_db)
):
    """
    Search blog posts with full-text search and filtering options
    
    - **q**: Search query (searches in title and content)
    - **category**: Filter by category name or slug
    - **tag**: Filter by tag name  
    - **author**: Filter by author username
    - **skip**: Pagination offset
    - **limit**: Number of results per page
    """
    
    # Start with base query for published posts
    query = db.query(BlogPost).filter(BlogPost.status == PostStatus.PUBLISHED)
    
    # Search in title and content
    search_terms = q.strip().split()
    if search_terms:
        search_conditions = []
        for term in search_terms:
            search_pattern = f"%{term}%"
            search_conditions.append(
                or_(
                    BlogPost.title.ilike(search_pattern),
                    BlogPost.content.ilike(search_pattern)
                )
            )
        # All terms should match (AND logic)
        query = query.filter(and_(*search_conditions))
    
    # Filter by category if specified
    if category:
        query = query.join(BlogPost.categories).filter(
            or_(
                Category.name.ilike(f"%{category}%"),
                Category.slug.ilike(f"%{category}%")
            )
        )
    
    # Filter by tag if specified  
    if tag:
        query = query.join(BlogPost.tags).filter(
            Tag.name.ilike(f"%{tag}%")
        )
    
    # Filter by author if specified
    if author:
        query = query.join(BlogPost.author).filter(
            User.username.ilike(f"%{author}%")
        )
    
    # Order by relevance (title matches first, then by date)
    # Simple ordering by published date for now
    query = query.order_by(BlogPost.published.desc())
    
    # Apply pagination
    posts = query.offset(skip).limit(limit).all()
    
    return posts

@router.get("/suggestions")
def get_search_suggestions(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(5, ge=1, le=10, description="Number of suggestions"),
    db: Session = Depends(get_db)
):
    """
    Get search suggestions based on partial query
    
    Returns suggestions from:
    - Blog post titles
    - Category names
    - Tag names
    - Author usernames
    """
    
    suggestions = []
    search_pattern = f"%{q}%"
    
    # Get title suggestions from published posts
    title_suggestions = db.query(BlogPost.title).filter(
        and_(
            BlogPost.title.ilike(search_pattern),
            BlogPost.status == PostStatus.PUBLISHED
        )
    ).limit(limit).all()
    
    for title in title_suggestions:
        suggestions.append({
            "text": title[0],
            "type": "title",
            "description": "Blog post title"
        })
    
    # Get category suggestions
    category_suggestions = db.query(Category.name).filter(
        Category.name.ilike(search_pattern)
    ).limit(limit).all()
    
    for category in category_suggestions:
        suggestions.append({
            "text": category[0],
            "type": "category", 
            "description": "Category"
        })
    
    # Get tag suggestions
    tag_suggestions = db.query(Tag.name).filter(
        Tag.name.ilike(search_pattern)
    ).limit(limit).all()
    
    for tag in tag_suggestions:
        suggestions.append({
            "text": tag[0],
            "type": "tag",
            "description": "Tag"
        })
    
    # Get author suggestions
    author_suggestions = db.query(User.username).filter(
        User.username.ilike(search_pattern)
    ).limit(limit).all()
    
    for author in author_suggestions:
        suggestions.append({
            "text": author[0],
            "type": "author",
            "description": "Author"
        })
    
    # Limit total suggestions and prioritize by type
    # (titles first, then categories, tags, authors)
    return suggestions[:limit]

@router.get("/filters")
def get_search_filters(db: Session = Depends(get_db)):
    """
    Get available search filters (categories, tags, authors)
    """
    
    # Get all categories
    categories = db.query(Category.name, Category.slug).all()
    
    # Get popular tags (with post count)
    tags = db.query(Tag.name, func.count(BlogPost.id).label('post_count')).join(
        BlogPost.tags
    ).group_by(Tag.id).order_by(func.count(BlogPost.id).desc()).limit(20).all()
    
    # Get active authors (with published post count)
    authors = db.query(User.username, func.count(BlogPost.id).label('post_count')).join(
        BlogPost, User.id == BlogPost.author_id
    ).filter(BlogPost.status == PostStatus.PUBLISHED).group_by(User.id).order_by(
        func.count(BlogPost.id).desc()
    ).limit(10).all()
    
    return {
        "categories": [{"name": cat[0], "slug": cat[1]} for cat in categories],
        "tags": [{"name": tag[0], "post_count": tag[1]} for tag in tags],
        "authors": [{"username": author[0], "post_count": author[1]} for author in authors]
    }