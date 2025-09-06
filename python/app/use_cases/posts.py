"""Post management use cases"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from app.domain.entities import BlogPost, PostStatus, User
from app.domain.errors import (
    PostNotFoundError,
    PostAlreadyExistsError, 
    UnauthorizedPostAccessError,
    PostNotPublishableError
)
from app.ports.repositories import PostReadRepository, PostWriteRepository
from app.ports.services import SlugGenerator


@dataclass
class CreatePostRequest:
    title: str
    content: str
    author_id: int
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    status: PostStatus = PostStatus.DRAFT


@dataclass
class UpdatePostRequest:
    post_id: int
    title: Optional[str] = None
    content: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    status: Optional[PostStatus] = None


@dataclass
class ListPostsRequest:
    skip: int = 0
    limit: int = 100
    author_id: Optional[int] = None
    published_only: bool = True


class CreatePostUseCase:
    """Use case for creating a new post"""
    
    def __init__(
        self,
        post_read_repository: PostReadRepository,
        post_write_repository: PostWriteRepository,
        slug_generator: SlugGenerator
    ):
        self.post_read_repository = post_read_repository
        self.post_write_repository = post_write_repository
        self.slug_generator = slug_generator
    
    def execute(self, request: CreatePostRequest) -> BlogPost:
        """Create a new blog post"""
        # Generate slug from title
        base_slug = self.slug_generator.generate_slug(request.title)
        
        # Ensure slug is unique
        existing_post = self.post_read_repository.get_by_slug(base_slug)
        if existing_post:
            # Generate unique slug
            counter = 1
            unique_slug = f"{base_slug}-{counter}"
            while self.post_read_repository.get_by_slug(unique_slug):
                counter += 1
                unique_slug = f"{base_slug}-{counter}"
            base_slug = unique_slug
        
        # Create post entity
        post = BlogPost(
            id=None,
            title=request.title,
            content=request.content,
            slug=base_slug,
            author_id=request.author_id,
            status=request.status,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            meta_title=request.meta_title,
            meta_description=request.meta_description
        )
        
        return self.post_write_repository.create(post)


class UpdatePostUseCase:
    """Use case for updating an existing post"""
    
    def __init__(
        self,
        post_read_repository: PostReadRepository,
        post_write_repository: PostWriteRepository,
        slug_generator: SlugGenerator
    ):
        self.post_read_repository = post_read_repository
        self.post_write_repository = post_write_repository
        self.slug_generator = slug_generator
    
    def execute(self, request: UpdatePostRequest, current_user: User) -> BlogPost:
        """Update an existing blog post"""
        # Get existing post
        post = self.post_read_repository.get_by_id(request.post_id)
        if not post:
            raise PostNotFoundError(str(request.post_id))
        
        # Check authorization
        if post.author_id != current_user.id and not current_user.can_moderate_posts():
            raise UnauthorizedPostAccessError("update")
        
        # Update fields if provided
        if request.title is not None:
            post.title = request.title
            # Regenerate slug if title changed
            new_slug = self.slug_generator.generate_slug(request.title)
            if new_slug != post.slug:
                # Check if new slug is available
                existing_post = self.post_read_repository.get_by_slug(new_slug)
                if existing_post and existing_post.id != post.id:
                    # Generate unique slug
                    counter = 1
                    unique_slug = f"{new_slug}-{counter}"
                    while self.post_read_repository.get_by_slug(unique_slug):
                        counter += 1
                        unique_slug = f"{new_slug}-{counter}"
                    post.slug = unique_slug
                else:
                    post.slug = new_slug
        
        if request.content is not None:
            post.content = request.content
        
        if request.meta_title is not None:
            post.meta_title = request.meta_title
        
        if request.meta_description is not None:
            post.meta_description = request.meta_description
        
        if request.status is not None:
            post.status = request.status
        
        post.updated_at = datetime.now()
        
        return self.post_write_repository.update(post)


class GetPostUseCase:
    """Use case for getting a single post"""
    
    def __init__(
        self,
        post_read_repository: PostReadRepository,
        post_write_repository: PostWriteRepository
    ):
        self.post_read_repository = post_read_repository
        self.post_write_repository = post_write_repository
    
    def execute(self, post_id: int, increment_views: bool = True) -> BlogPost:
        """Get a post by ID and optionally increment view count"""
        post = self.post_read_repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))
        
        if increment_views and post.is_published():
            self.post_write_repository.increment_view_count(post_id)
            post.view_count += 1
        
        return post


class GetPostBySlugUseCase:
    """Use case for getting a post by slug"""
    
    def __init__(
        self,
        post_read_repository: PostReadRepository,
        post_write_repository: PostWriteRepository
    ):
        self.post_read_repository = post_read_repository
        self.post_write_repository = post_write_repository
    
    def execute(self, slug: str, increment_views: bool = True) -> BlogPost:
        """Get a post by slug and optionally increment view count"""
        post = self.post_read_repository.get_by_slug(slug)
        if not post:
            raise PostNotFoundError(slug)
        
        if increment_views and post.is_published():
            self.post_write_repository.increment_view_count(post.id)
            post.view_count += 1
        
        return post


class ListPostsUseCase:
    """Use case for listing posts"""
    
    def __init__(self, post_read_repository: PostReadRepository):
        self.post_read_repository = post_read_repository
    
    def execute(self, request: ListPostsRequest) -> List[BlogPost]:
        """List posts based on criteria"""
        if request.published_only:
            return self.post_read_repository.list_published(
                skip=request.skip,
                limit=request.limit,
                author_id=request.author_id
            )
        elif request.author_id:
            return self.post_read_repository.list_by_author(
                author_id=request.author_id,
                skip=request.skip,
                limit=request.limit
            )
        else:
            # For non-published, we need author_id for authorization
            raise ValueError("author_id required when listing non-published posts")


class DeletePostUseCase:
    """Use case for deleting a post"""
    
    def __init__(
        self,
        post_read_repository: PostReadRepository,
        post_write_repository: PostWriteRepository
    ):
        self.post_read_repository = post_read_repository
        self.post_write_repository = post_write_repository
    
    def execute(self, post_id: int, current_user: User) -> bool:
        """Delete a post"""
        # Get existing post
        post = self.post_read_repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))
        
        # Check authorization
        if post.author_id != current_user.id and not current_user.can_moderate_posts():
            raise UnauthorizedPostAccessError("delete")
        
        return self.post_write_repository.delete(post_id)


class PublishPostUseCase:
    """Use case for publishing a post"""
    
    def __init__(
        self,
        post_read_repository: PostReadRepository,
        post_write_repository: PostWriteRepository
    ):
        self.post_read_repository = post_read_repository
        self.post_write_repository = post_write_repository
    
    def execute(self, post_id: int, current_user: User) -> BlogPost:
        """Publish a post"""
        # Get existing post
        post = self.post_read_repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))
        
        # Check authorization
        if post.author_id != current_user.id and not current_user.can_moderate_posts():
            raise UnauthorizedPostAccessError("publish")
        
        # Check if post can be published
        if not post.can_be_published():
            raise PostNotPublishableError(f"Post status is {post.status}")
        
        # Publish the post
        post.publish()
        post.updated_at = datetime.now()
        
        return self.post_write_repository.update(post)