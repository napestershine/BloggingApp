"""SQLAlchemy implementation of post repository ports"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.domain.entities import BlogPost as PostEntity, PostStatus
from app.domain.errors import PostNotFoundError, PostAlreadyExistsError
from app.models.models import BlogPost as PostModel
from app.ports.repositories import PostReadRepository, PostWriteRepository


class SqlAlchemyPostReadRepository:
    """SQLAlchemy implementation of PostReadRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, post_id: int) -> Optional[PostEntity]:
        """Get post by ID"""
        db_post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
        return self._to_entity(db_post) if db_post else None
    
    def get_by_slug(self, slug: str) -> Optional[PostEntity]:
        """Get post by slug"""
        db_post = self.db.query(PostModel).filter(PostModel.slug == slug).first()
        return self._to_entity(db_post) if db_post else None
    
    def list_published(
        self, 
        skip: int = 0, 
        limit: int = 100,
        author_id: Optional[int] = None
    ) -> List[PostEntity]:
        """List published posts"""
        query = self.db.query(PostModel).filter(PostModel.status == PostStatus.PUBLISHED)
        
        if author_id:
            query = query.filter(PostModel.author_id == author_id)
        
        db_posts = query.offset(skip).limit(limit).all()
        return [self._to_entity(post) for post in db_posts]
    
    def list_by_author(
        self, 
        author_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[PostEntity]:
        """List posts by author (including drafts)"""
        db_posts = (
            self.db.query(PostModel)
            .filter(PostModel.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(post) for post in db_posts]
    
    def search(
        self, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[PostEntity]:
        """Search posts by title/content"""
        db_posts = (
            self.db.query(PostModel)
            .filter(
                PostModel.status == PostStatus.PUBLISHED,
                or_(
                    PostModel.title.ilike(f"%{query}%"),
                    PostModel.content.ilike(f"%{query}%")
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(post) for post in db_posts]
    
    def _to_entity(self, db_post: PostModel) -> PostEntity:
        """Convert SQLAlchemy model to domain entity"""
        return PostEntity(
            id=db_post.id,
            title=db_post.title,
            content=db_post.content,
            slug=db_post.slug,
            author_id=db_post.author_id,
            status=db_post.status,
            created_at=db_post.published,  # Note: using 'published' field as created_at
            updated_at=db_post.last_modified,
            published_at=db_post.published if db_post.status == PostStatus.PUBLISHED else None,
            meta_title=db_post.meta_title,
            meta_description=db_post.meta_description,
            view_count=db_post.view_count,
            featured=db_post.featured
        )


class SqlAlchemyPostWriteRepository:
    """SQLAlchemy implementation of PostWriteRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, post: PostEntity) -> PostEntity:
        """Create a new post"""
        # Check for existing post with same slug
        if post.slug and self.db.query(PostModel).filter(PostModel.slug == post.slug).first():
            raise PostAlreadyExistsError("slug", post.slug)
        
        # Convert domain entity to SQLAlchemy model
        db_post = PostModel(
            title=post.title,
            content=post.content,
            slug=post.slug,
            author_id=post.author_id,
            status=post.status,
            meta_title=post.meta_title,
            meta_description=post.meta_description,
            view_count=post.view_count,
            featured=post.featured
        )
        
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        
        # Convert back to domain entity
        return self._to_entity(db_post)
    
    def update(self, post: PostEntity) -> PostEntity:
        """Update existing post"""
        if not post.id:
            raise ValueError("Post ID is required for update")
        
        db_post = self.db.query(PostModel).filter(PostModel.id == post.id).first()
        if not db_post:
            raise PostNotFoundError(str(post.id))
        
        # Update fields
        db_post.title = post.title
        db_post.content = post.content
        db_post.slug = post.slug
        db_post.status = post.status
        db_post.meta_title = post.meta_title
        db_post.meta_description = post.meta_description
        db_post.view_count = post.view_count
        db_post.featured = post.featured
        
        self.db.commit()
        self.db.refresh(db_post)
        
        return self._to_entity(db_post)
    
    def delete(self, post_id: int) -> bool:
        """Delete post by ID"""
        db_post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
        if not db_post:
            return False
        
        self.db.delete(db_post)
        self.db.commit()
        return True
    
    def increment_view_count(self, post_id: int) -> None:
        """Increment post view count"""
        db_post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
        if db_post:
            db_post.view_count += 1
            self.db.commit()
    
    def _to_entity(self, db_post: PostModel) -> PostEntity:
        """Convert SQLAlchemy model to domain entity"""
        return PostEntity(
            id=db_post.id,
            title=db_post.title,
            content=db_post.content,
            slug=db_post.slug,
            author_id=db_post.author_id,
            status=db_post.status,
            created_at=db_post.published,
            updated_at=db_post.last_modified,
            published_at=db_post.published if db_post.status == PostStatus.PUBLISHED else None,
            meta_title=db_post.meta_title,
            meta_description=db_post.meta_description,
            view_count=db_post.view_count,
            featured=db_post.featured
        )