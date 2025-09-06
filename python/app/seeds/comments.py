"""
Comment seeder for creating sample comments
"""
from .base import BaseSeeder
from app.models.comment import Comment, CommentStatus
from app.models.blog_post import BlogPost
from app.models.user import User
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CommentSeeder(BaseSeeder):
    """Seeder for creating sample comments"""
    
    def seed(self):
        """Create sample comments"""
        # Get posts and users for commenting
        welcome_post = self.db.query(BlogPost).filter(BlogPost.slug == "welcome-to-our-blog-platform").first()
        blogging_post = self.db.query(BlogPost).filter(BlogPost.slug == "getting-started-with-blogging").first()
        tech_post = self.db.query(BlogPost).filter(BlogPost.slug == "the-future-of-web-development").first()
        
        user1 = self.db.query(User).filter(User.username == "user1").first()
        user2 = self.db.query(User).filter(User.username == "user2").first()
        editor = self.db.query(User).filter(User.username == "editor").first()
        
        if not welcome_post or not user1:
            logger.warning("Required posts or users not found, skipping comment seeding")
            return
        
        comments_data = [
            {
                "content": "Welcome to the platform! This looks amazing. I'm excited to start blogging here.",
                "blog_post": welcome_post,
                "author": user1,
                "status": CommentStatus.APPROVED
            },
            {
                "content": "Great platform! The interface is very user-friendly. Looking forward to contributing.",
                "blog_post": welcome_post,
                "author": user2 or user1,
                "status": CommentStatus.APPROVED
            },
            {
                "content": "Thanks for the warm welcome! Can't wait to explore all the features.",
                "blog_post": welcome_post,
                "author": editor or user1,
                "status": CommentStatus.APPROVED
            }
        ]
        
        if blogging_post:
            comments_data.extend([
                {
                    "content": "These are excellent tips! I especially appreciate the advice about consistency. It's something I struggle with.",
                    "blog_post": blogging_post,
                    "author": user1,
                    "status": CommentStatus.APPROVED
                },
                {
                    "content": "Finding your niche is indeed crucial. It took me months to figure out what I was passionate about writing.",
                    "blog_post": blogging_post,
                    "author": user2 or user1,
                    "status": CommentStatus.APPROVED
                }
            ])
        
        if tech_post:
            comments_data.extend([
                {
                    "content": "WebAssembly is indeed fascinating! I've been experimenting with it lately. The performance gains are impressive.",
                    "blog_post": tech_post,
                    "author": editor or user1,
                    "status": CommentStatus.APPROVED
                },
                {
                    "content": "AI integration in development tools has been a game-changer for my productivity. Great insights!",
                    "blog_post": tech_post,
                    "author": user1,
                    "status": CommentStatus.APPROVED
                }
            ])
        
        created_count = 0
        for i, comment_data in enumerate(comments_data):
            blog_post = comment_data.pop("blog_post")
            author = comment_data.pop("author")
            
            comment, created = self.get_or_create(
                Comment,
                content=comment_data["content"],
                blog_post_id=blog_post.id,
                author_id=author.id,
                defaults={
                    **comment_data,
                    "blog_post_id": blog_post.id,
                    "author_id": author.id,
                    "published": datetime.utcnow() - timedelta(hours=i)  # Spread out comment times
                }
            )
            
            if created:
                created_count += 1
                logger.info(f"Created comment by {author.username} on {blog_post.title}")
            else:
                logger.info(f"Comment already exists by {author.username}")
        
        logger.info(f"Comment seeding completed. Created {created_count} new comments.")
    
    def clear(self):
        """Remove seeded comments"""
        # Find comments on seeded posts
        seeded_post_slugs = [
            "welcome-to-our-blog-platform",
            "getting-started-with-blogging",
            "the-future-of-web-development"
        ]
        
        deleted_count = 0
        for slug in seeded_post_slugs:
            post = self.db.query(BlogPost).filter(BlogPost.slug == slug).first()
            if post:
                comments = self.db.query(Comment).filter(Comment.blog_post_id == post.id).all()
                for comment in comments:
                    self.db.delete(comment)
                    deleted_count += 1
                    logger.info(f"Deleted comment: {comment.content[:50]}...")
        
        self.safe_commit()
        logger.info(f"Comment clearing completed. Deleted {deleted_count} comments.")
