from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import BlogPost
from app.schemas.schemas import SEOData, SEOPreview
from fastapi import HTTPException
import re

class SEOService:
    
    def get_post_seo(self, db: Session, post_id: int) -> SEOData:
        """
        Get SEO data for a specific post
        """
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        return SEOData(
            meta_title=post.meta_title,
            meta_description=post.meta_description,
            og_title=post.og_title,
            og_description=post.og_description,
            og_image=post.og_image
        )
    
    def update_post_seo(self, db: Session, post_id: int, seo_data: SEOData, user_id: int) -> SEOData:
        """
        Update SEO data for a specific post
        """
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Check if user owns the post
        if post.author_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this post")
        
        # Update SEO fields
        post.meta_title = seo_data.meta_title
        post.meta_description = seo_data.meta_description
        post.og_title = seo_data.og_title
        post.og_description = seo_data.og_description
        post.og_image = seo_data.og_image
        
        db.commit()
        db.refresh(post)
        
        return SEOData(
            meta_title=post.meta_title,
            meta_description=post.meta_description,
            og_title=post.og_title,
            og_description=post.og_description,
            og_image=post.og_image
        )
    
    def generate_seo_preview(self, db: Session, post_id: int, base_url: str = "https://example.com") -> SEOPreview:
        """
        Generate SEO preview for a post (how it would appear in search results/social media)
        """
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Use meta title or fall back to post title
        title = post.meta_title or post.title
        
        # Use meta description or generate from content
        description = post.meta_description
        if not description:
            # Generate description from content (first 160 characters)
            clean_content = re.sub(r'<[^>]+>', '', post.content)  # Remove HTML tags
            description = clean_content[:157] + "..." if len(clean_content) > 160 else clean_content
        
        # Use og_image or a default
        image = post.og_image
        
        # Generate URL
        url = f"{base_url}/posts/{post.slug or post.id}"
        
        return SEOPreview(
            title=title,
            description=description,
            url=url,
            image=image
        )
    
    def validate_seo_data(self, seo_data: SEOData) -> dict:
        """
        Validate SEO data and provide recommendations
        """
        issues = []
        recommendations = []
        
        # Check meta title
        if seo_data.meta_title:
            if len(seo_data.meta_title) > 60:
                issues.append("Meta title is too long (over 60 characters)")
            elif len(seo_data.meta_title) < 30:
                recommendations.append("Consider making meta title longer (30-60 characters is ideal)")
        else:
            recommendations.append("Add a meta title for better SEO")
        
        # Check meta description
        if seo_data.meta_description:
            if len(seo_data.meta_description) > 160:
                issues.append("Meta description is too long (over 160 characters)")
            elif len(seo_data.meta_description) < 120:
                recommendations.append("Consider making meta description longer (120-160 characters is ideal)")
        else:
            recommendations.append("Add a meta description for better SEO")
        
        # Check Open Graph data
        if not seo_data.og_title:
            recommendations.append("Add Open Graph title for better social media sharing")
        
        if not seo_data.og_description:
            recommendations.append("Add Open Graph description for better social media sharing")
        
        if not seo_data.og_image:
            recommendations.append("Add Open Graph image for better social media sharing")
        
        return {
            "issues": issues,
            "recommendations": recommendations,
            "score": max(0, 100 - len(issues) * 20 - len(recommendations) * 5)
        }