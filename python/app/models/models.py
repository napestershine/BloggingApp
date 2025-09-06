# This file maintains backward compatibility by re-importing from the new modular structure
# All models have been moved to separate files for better organization

from .user import User, UserRole
from .blog_post import BlogPost, PostStatus, blog_post_tags, blog_post_categories
from .comment import Comment, CommentStatus, CommentReaction, ReactionType
from .media import Media
from .category import Category
from .tag import Tag
from .post_engagement import PostLike, PostShare, SharingPlatform

# Import Base for table creation in main.py
from app.database.connection import Base
