from typing import List
from sqlalchemy.orm import Session
from app.models.models import BlogPost
from datetime import datetime
import xml.etree.ElementTree as ET

class SitemapService:
    
    def generate_sitemap_xml(self, db: Session, base_url: str = "https://example.com") -> str:
        """
        Generate XML sitemap for all blog posts
        """
        # Create root element
        urlset = ET.Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        
        # Add homepage
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = base_url
        ET.SubElement(url, "changefreq").text = "daily"
        ET.SubElement(url, "priority").text = "1.0"
        
        # Add blog posts
        posts = db.query(BlogPost).order_by(BlogPost.published.desc()).all()
        
        for post in posts:
            url = ET.SubElement(urlset, "url")
            
            # URL location
            post_url = f"{base_url}/posts/{post.slug or post.id}"
            ET.SubElement(url, "loc").text = post_url
            
            # Last modification date
            lastmod = post.updated_at or post.published
            ET.SubElement(url, "lastmod").text = lastmod.isoformat()
            
            # Change frequency
            ET.SubElement(url, "changefreq").text = "weekly"
            
            # Priority based on view count
            view_count = post.view_count or 0
            if view_count > 1000:
                priority = "0.9"
            elif view_count > 100:
                priority = "0.8"
            elif view_count > 10:
                priority = "0.7"
            else:
                priority = "0.6"
            
            ET.SubElement(url, "priority").text = priority
        
        # Convert to string
        return self._prettify_xml(urlset)
    
    def get_sitemap_posts(self, db: Session) -> List[dict]:
        """
        Get sitemap data for posts in JSON format
        """
        posts = db.query(BlogPost).order_by(BlogPost.published.desc()).all()
        
        sitemap_posts = []
        for post in posts:
            sitemap_posts.append({
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "published": post.published.isoformat(),
                "updated": post.updated_at.isoformat() if post.updated_at else post.published.isoformat(),
                "view_count": post.view_count or 0,
                "category": post.category,
                "author": post.author.username
            })
        
        return sitemap_posts
    
    def _prettify_xml(self, elem) -> str:
        """
        Return a pretty-printed XML string for the Element.
        """
        from xml.dom import minidom
        rough_string = ET.tostring(elem, 'unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def generate_robots_txt(self, base_url: str = "https://example.com") -> str:
        """
        Generate robots.txt content
        """
        return f"""User-agent: *
Allow: /

# Sitemap
Sitemap: {base_url}/api/sitemap.xml

# Disallow admin areas (if any)
Disallow: /admin/
Disallow: /api/auth/
"""