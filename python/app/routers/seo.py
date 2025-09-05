from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.models import User
from app.auth.auth import get_current_user
from app.schemas.schemas import SEOData, SEOPreview
from app.services.seo_service import SEOService

router = APIRouter(prefix="/seo", tags=["seo"])
seo_service = SEOService()

@router.get("/posts/{post_id}", response_model=SEOData)
def get_post_seo(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Get SEO data for a specific post
    """
    return seo_service.get_post_seo(db, post_id)

@router.put("/posts/{post_id}", response_model=SEOData)
def update_post_seo(
    post_id: int,
    seo_data: SEOData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update SEO data for a specific post
    """
    return seo_service.update_post_seo(db, post_id, seo_data, current_user.id)

@router.get("/posts/{post_id}/preview", response_model=SEOPreview)
def get_seo_preview(
    post_id: int,
    base_url: str = "https://example.com",
    db: Session = Depends(get_db)
):
    """
    Generate SEO preview for a post (how it would appear in search results/social media)
    """
    return seo_service.generate_seo_preview(db, post_id, base_url)

@router.post("/validate")
def validate_seo_data(seo_data: SEOData):
    """
    Validate SEO data and provide recommendations
    """
    return seo_service.validate_seo_data(seo_data)