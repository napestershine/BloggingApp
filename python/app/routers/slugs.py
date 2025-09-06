from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.schemas import SlugValidation, SlugSuggestion
from app.services.slug_service import SlugService

router = APIRouter(prefix="/slugs", tags=["slugs"])
slug_service = SlugService()

@router.get("/validate", response_model=SlugValidation)
def validate_slug(
    slug: str = Query(..., description="Slug to validate"),
    exclude_post_id: int = Query(None, description="Post ID to exclude from validation"),
    db: Session = Depends(get_db)
):
    """
    Validate if a slug is available and provide suggestions if not
    """
    return slug_service.validate_slug(db, slug, exclude_post_id)

@router.get("/suggest", response_model=SlugSuggestion)
def suggest_slugs(
    title: str = Query(..., description="Post title to generate slug suggestions from"),
    db: Session = Depends(get_db)
):
    """
    Generate slug suggestions based on a title
    """
    return slug_service.suggest_slugs(db, title)