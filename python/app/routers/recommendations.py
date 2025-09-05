from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, or_
from app.database.connection import get_db
from app.models.models import BlogPost, User
from app.schemas.schemas import BlogPost as BlogPostSchema, TrendingPost, RelatedPost
import json

router = APIRouter(tags=["recommendations"])

@router.get("/posts/{post_id}/related", response_model=List[BlogPostSchema])
def get_related_posts(
    post_id: int,
    limit: int = Query(5, ge=1, le=20, description="Number of related posts to return"),
    db: Session = Depends(get_db)
):
    """
    Get related posts based on content similarity
    """
    # Get the current post
    current_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not current_post:
        return []
    
    # Simple similarity based on category and tags
    related_query = db.query(BlogPost).filter(BlogPost.id != post_id)
    
    # If post has category, prioritize same category
    if current_post.category:
        related_query = related_query.filter(BlogPost.category == current_post.category)
    
    # If post has tags, find posts with similar tags
    if current_post.tags:
        try:
            current_tags = json.loads(current_post.tags) if isinstance(current_post.tags, str) else current_post.tags
            if isinstance(current_tags, list):
                for tag in current_tags:
                    related_query = related_query.filter(BlogPost.tags.ilike(f"%{tag}%"))
        except (json.JSONDecodeError, TypeError):
            pass
    
    # Order by view count and recency
    related_posts = related_query.order_by(
        desc(BlogPost.view_count),
        desc(BlogPost.published)
    ).limit(limit).all()
    
    return related_posts

@router.get("/posts/trending", response_model=List[BlogPostSchema])
def get_trending_posts(
    limit: int = Query(10, ge=1, le=50, description="Number of trending posts to return"),
    days: int = Query(7, ge=1, le=30, description="Time period in days to consider"),
    db: Session = Depends(get_db)
):
    """
    Get trending posts based on view count and engagement
    """
    # Simple trending algorithm based on view count
    # In a real implementation, you might consider:
    # - Recent views (weighted by recency)
    # - Comment count
    # - Social shares
    # - Time since publication
    
    trending_posts = db.query(BlogPost).filter(
        BlogPost.view_count > 0
    ).order_by(
        desc(BlogPost.view_count),
        desc(BlogPost.published)
    ).limit(limit).all()
    
    return trending_posts

@router.get("/topics/hot")
def get_hot_topics(
    limit: int = Query(10, ge=1, le=20, description="Number of hot topics to return"),
    db: Session = Depends(get_db)
):
    """
    Get hot topics based on post frequency and engagement
    """
    # Get most frequent categories
    category_counts = db.query(
        BlogPost.category,
        func.count(BlogPost.id).label('post_count'),
        func.sum(BlogPost.view_count).label('total_views')
    ).filter(
        BlogPost.category.isnot(None)
    ).group_by(BlogPost.category).order_by(
        desc('total_views'),
        desc('post_count')
    ).limit(limit).all()
    
    hot_topics = []
    for category, post_count, total_views in category_counts:
        hot_topics.append({
            "topic": category,
            "post_count": post_count,
            "total_views": total_views or 0,
            "score": (total_views or 0) + (post_count * 10)  # Simple scoring
        })
    
    # Get most frequent tags
    tags_data = db.query(BlogPost.tags).filter(BlogPost.tags.isnot(None)).all()
    tag_counts = {}
    
    for tag_row in tags_data:
        if tag_row[0]:
            try:
                tags = json.loads(tag_row[0]) if isinstance(tag_row[0], str) else tag_row[0]
                if isinstance(tags, list):
                    for tag in tags:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
                elif isinstance(tags, str):
                    for tag in tags.split(','):
                        tag = tag.strip()
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
            except (json.JSONDecodeError, TypeError):
                if isinstance(tag_row[0], str):
                    for tag in tag_row[0].split(','):
                        tag = tag.strip()
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Add top tags to hot topics
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for tag, count in sorted_tags:
        hot_topics.append({
            "topic": tag,
            "post_count": count,
            "total_views": 0,
            "score": count * 5,
            "type": "tag"
        })
    
    return {
        "hot_topics": sorted(hot_topics, key=lambda x: x["score"], reverse=True)[:limit],
        "generated_at": "2024-01-01T00:00:00Z"
    }