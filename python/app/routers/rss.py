from typing import Optional
from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.connection import get_db
from app.models.models import BlogPost
from datetime import datetime
import xml.etree.ElementTree as ET

router = APIRouter(prefix="/rss", tags=["rss"])

@router.get("/")
def get_rss_feed(
    base_url: str = Query("https://example.com", description="Base URL for the blog"),
    limit: int = Query(20, ge=1, le=100, description="Number of posts to include"),
    db: Session = Depends(get_db)
):
    """
    Generate RSS feed for all blog posts
    """
    posts = db.query(BlogPost).order_by(desc(BlogPost.published)).limit(limit).all()
    
    rss_content = _generate_rss_xml(posts, base_url, "Blog Feed", "Latest blog posts")
    
    return Response(
        content=rss_content,
        media_type="application/rss+xml",
        headers={"Content-Disposition": "inline; filename=rss.xml"}
    )

@router.get("/categories/{category}")
def get_category_rss_feed(
    category: str,
    base_url: str = Query("https://example.com", description="Base URL for the blog"),
    limit: int = Query(20, ge=1, le=100, description="Number of posts to include"),
    db: Session = Depends(get_db)
):
    """
    Generate RSS feed for posts in a specific category
    """
    posts = db.query(BlogPost).filter(
        BlogPost.category == category
    ).order_by(desc(BlogPost.published)).limit(limit).all()
    
    if not posts:
        # Return empty RSS feed if no posts found
        posts = []
    
    title = f"Blog Feed - {category.title()}"
    description = f"Latest blog posts in {category} category"
    rss_content = _generate_rss_xml(posts, base_url, title, description)
    
    return Response(
        content=rss_content,
        media_type="application/rss+xml",
        headers={"Content-Disposition": f"inline; filename=rss-{category}.xml"}
    )

@router.get("/authors/{author_username}")
def get_author_rss_feed(
    author_username: str,
    base_url: str = Query("https://example.com", description="Base URL for the blog"),
    limit: int = Query(20, ge=1, le=100, description="Number of posts to include"),
    db: Session = Depends(get_db)
):
    """
    Generate RSS feed for posts by a specific author
    """
    posts = db.query(BlogPost).join(BlogPost.author).filter(
        BlogPost.author.has(username=author_username)
    ).order_by(desc(BlogPost.published)).limit(limit).all()
    
    if not posts:
        posts = []
    
    title = f"Blog Feed - {author_username}"
    description = f"Latest blog posts by {author_username}"
    rss_content = _generate_rss_xml(posts, base_url, title, description)
    
    return Response(
        content=rss_content,
        media_type="application/rss+xml",
        headers={"Content-Disposition": f"inline; filename=rss-{author_username}.xml"}
    )

def _generate_rss_xml(posts, base_url: str, title: str, description: str) -> str:
    """
    Generate RSS XML content from blog posts
    """
    # Create RSS root element
    rss = ET.Element("rss")
    rss.set("version", "2.0")
    rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
    
    # Create channel element
    channel = ET.SubElement(rss, "channel")
    
    # Channel metadata
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = base_url
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    ET.SubElement(channel, "generator").text = "BloggingApp RSS Generator"
    
    # Self-referencing link
    atom_link = ET.SubElement(channel, "atom:link")
    atom_link.set("href", f"{base_url}/api/rss/")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")
    
    # Add items for each post
    for post in posts:
        item = ET.SubElement(channel, "item")
        
        # Post metadata
        ET.SubElement(item, "title").text = post.title
        ET.SubElement(item, "link").text = f"{base_url}/posts/{post.slug or post.id}"
        ET.SubElement(item, "guid").text = f"{base_url}/posts/{post.slug or post.id}"
        ET.SubElement(item, "pubDate").text = post.published.strftime("%a, %d %b %Y %H:%M:%S GMT")
        ET.SubElement(item, "author").text = f"{post.author.email} ({post.author.name})"
        
        # Post content
        description_elem = ET.SubElement(item, "description")
        # Use meta description if available, otherwise truncate content
        if post.meta_description:
            description_elem.text = post.meta_description
        else:
            # Strip HTML and truncate to 200 characters
            import re
            clean_content = re.sub(r'<[^>]+>', '', post.content)
            description_elem.text = clean_content[:200] + "..." if len(clean_content) > 200 else clean_content
        
        # Full content
        content_elem = ET.SubElement(item, "content:encoded")
        content_elem.text = f"<![CDATA[{post.content}]]>"
        
        # Category
        if post.category:
            ET.SubElement(item, "category").text = post.category
    
    # Convert to string and prettify
    return _prettify_xml(rss)

def _prettify_xml(elem) -> str:
    """
    Return a pretty-printed XML string for the Element.
    """
    from xml.dom import minidom
    rough_string = ET.tostring(elem, 'unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")