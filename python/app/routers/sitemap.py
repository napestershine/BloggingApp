from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.sitemap_service import SitemapService

router = APIRouter(tags=["sitemap"])
sitemap_service = SitemapService()

@router.get("/sitemap.xml")
def get_sitemap_xml(
    base_url: str = "https://example.com",
    db: Session = Depends(get_db)
):
    """
    Generate XML sitemap for search engines
    """
    xml_content = sitemap_service.generate_sitemap_xml(db, base_url)
    
    return Response(
        content=xml_content,
        media_type="application/xml",
        headers={"Content-Disposition": "inline; filename=sitemap.xml"}
    )

@router.get("/sitemap/posts")
def get_sitemap_posts(db: Session = Depends(get_db)):
    """
    Get sitemap data for posts in JSON format
    """
    return {
        "posts": sitemap_service.get_sitemap_posts(db),
        "generated_at": "2024-01-01T00:00:00Z"  # You could use actual timestamp
    }

@router.get("/robots.txt")
def get_robots_txt(base_url: str = "https://example.com"):
    """
    Generate robots.txt content
    """
    robots_content = sitemap_service.generate_robots_txt(base_url)
    
    return Response(
        content=robots_content,
        media_type="text/plain",
        headers={"Content-Disposition": "inline; filename=robots.txt"}
    )