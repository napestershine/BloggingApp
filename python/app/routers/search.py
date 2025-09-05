from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.schemas import SearchQuery, SearchResult, SearchSuggestion
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])
search_service = SearchService()

@router.get("/", response_model=SearchResult)
def search_posts(
    q: str = Query(..., description="Search query"),
    category: str = Query(None, description="Filter by category"),
    tags: List[str] = Query(None, description="Filter by tags"),
    author: str = Query(None, description="Filter by author name/username"),
    sort_by: str = Query("relevance", description="Sort by: relevance, date, views, updated"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    Search blog posts with filters and sorting
    """
    search_query = SearchQuery(
        q=q,
        category=category,
        tags=tags or [],
        author=author,
        sort_by=sort_by,
        limit=limit,
        offset=offset
    )
    
    return search_service.search_posts(db, search_query)

@router.get("/suggestions", response_model=SearchSuggestion)
def get_search_suggestions(
    q: str = Query(..., description="Partial search query"),
    db: Session = Depends(get_db)
):
    """
    Get search suggestions based on partial query
    """
    return search_service.get_search_suggestions(db, q)

@router.get("/filters")
def get_search_filters(db: Session = Depends(get_db)):
    """
    Get available search filters (categories, tags, authors)
    """
    return search_service.get_search_filters(db)