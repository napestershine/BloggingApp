"""
Blog post seeder for creating sample posts
"""
from .base import BaseSeeder
from app.models.blog_post import BlogPost, PostStatus
from app.models.user import User
from app.services.slug_service import SlugService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class PostSeeder(BaseSeeder):
    """Seeder for creating sample blog posts"""
    
    def seed(self):
        """Create sample blog posts"""
        # Get users for authoring posts
        admin_user = self.db.query(User).filter(User.username == "admin").first()
        editor_user = self.db.query(User).filter(User.username == "editor").first()
        user1 = self.db.query(User).filter(User.username == "user1").first()
        
        if not admin_user:
            logger.warning("Admin user not found, skipping post seeding")
            return
        
        posts_data = [
            {
                "title": "Welcome to Our Blog Platform",
                "content": """Welcome to our amazing blog platform! This is a sample post to demonstrate the features of our blogging application.

## Features

- User registration and authentication
- Rich text editing
- Comment system
- User profiles
- Search functionality

We hope you enjoy using our platform!""",
                "author": admin_user,
                "status": PostStatus.PUBLISHED,
                "category": "Announcements",
                "tags": "welcome,announcement,platform",
                "meta_title": "Welcome to Our Blog Platform - Get Started Today",
                "meta_description": "Discover the features of our blog platform and start your blogging journey.",
                "featured": True
            },
            {
                "title": "Getting Started with Blogging",
                "content": """Starting a blog can be exciting and rewarding. Here are some tips to help you get started:

## 1. Choose Your Niche

Pick a topic you're passionate about and knowledgeable in.

## 2. Create Quality Content

Focus on providing value to your readers with well-researched, engaging posts.

## 3. Be Consistent

Regular posting keeps your audience engaged and coming back for more.

## 4. Engage with Your Community

Respond to comments and interact with other bloggers in your niche.

Happy blogging!""",
                "author": editor_user or admin_user,
                "status": PostStatus.PUBLISHED,
                "category": "Tips",
                "tags": "blogging,tips,beginners",
                "meta_title": "Getting Started with Blogging - Tips for Beginners",
                "meta_description": "Learn essential tips for starting your blogging journey and building an engaged audience."
            },
            {
                "title": "The Future of Web Development",
                "content": """Web development continues to evolve at a rapid pace. Let's explore some trends shaping the future:

## Modern Frameworks

- React, Vue, and Angular continue to dominate
- New frameworks like Svelte are gaining traction
- Server-side rendering is making a comeback

## WebAssembly

WebAssembly (WASM) is enabling near-native performance in browsers.

## AI Integration

AI tools are transforming how developers write code and solve problems.

## Progressive Web Apps

PWAs bridge the gap between web and native applications.

The future looks bright for web developers!""",
                "author": user1 or admin_user,
                "status": PostStatus.PUBLISHED,
                "category": "Technology",
                "tags": "web-development,technology,future,programming",
                "meta_title": "The Future of Web Development - Trends to Watch",
                "meta_description": "Explore emerging trends in web development and what the future holds for developers."
            },
            {
                "title": "Draft Post - Work in Progress",
                "content": """This is a draft post that's still being worked on.

## Outline

- Introduction
- Main points (to be added)
- Conclusion (to be written)

This post will be published once it's complete.""",
                "author": editor_user or admin_user,
                "status": PostStatus.DRAFT,
                "category": "Drafts",
                "tags": "draft,work-in-progress"
            }
        ]
        
        slug_service = SlugService()
        created_count = 0
        
        for post_data in posts_data:
            author = post_data.pop("author")
            # Generate slug from title
            slug = slug_service._clean_slug(post_data["title"])
            
            post, created = self.get_or_create(
                BlogPost,
                slug=slug,
                defaults={
                    **post_data,
                    "author_id": author.id,
                    "slug": slug,
                    "published": datetime.utcnow() - timedelta(days=created_count)  # Spread out publish dates
                }
            )
            
            if created:
                created_count += 1
                logger.info(f"Created post: {post.title}")
            else:
                logger.info(f"Post already exists: {post.title}")
        
        logger.info(f"Post seeding completed. Created {created_count} new posts.")
    
    def clear(self):
        """Remove seeded posts"""
        seeded_slugs = [
            "welcome-to-our-blog-platform",
            "getting-started-with-blogging", 
            "the-future-of-web-development",
            "draft-post-work-in-progress"
        ]
        
        deleted_count = 0
        for slug in seeded_slugs:
            post = self.db.query(BlogPost).filter(BlogPost.slug == slug).first()
            if post:
                self.db.delete(post)
                deleted_count += 1
                logger.info(f"Deleted post: {post.title}")
        
        self.safe_commit()
        logger.info(f"Post clearing completed. Deleted {deleted_count} posts.")
