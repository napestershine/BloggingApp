"""Posts router using SOLID architecture"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.config.container import get_container
from app.presentation.schemas import (
    PostCreateRequest, PostUpdateRequest, PostResponse, PostListResponse,
    SuccessResponse
)
from app.presentation.routers.auth import get_current_user
from app.use_cases.posts import (
    CreatePostRequest, UpdatePostRequest, ListPostsRequest
)
from app.domain.errors import (
    PostNotFoundError, PostAlreadyExistsError, UnauthorizedPostAccessError,
    PostNotPublishableError, DomainError
)
from app.domain.entities import User, BlogPost

router = APIRouter(prefix="/posts", tags=["posts"])


def map_post_to_response(post: BlogPost) -> PostResponse:
    """Map domain post entity to response schema"""
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        slug=post.slug,
        author_id=post.author_id,
        status=post.status,
        created_at=post.created_at,
        updated_at=post.updated_at,
        published_at=post.published_at,
        meta_title=post.meta_title,
        meta_description=post.meta_description,
        view_count=post.view_count,
        featured=post.featured
    )


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    request: PostCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post"""
    container = get_container(db)
    use_case = container.create_post_use_case()
    
    try:
        # Map request to use case request
        use_case_request = CreatePostRequest(
            title=request.title,
            content=request.content,
            author_id=current_user.id,
            meta_title=request.meta_title,
            meta_description=request.meta_description,
            status=request.status
        )
        
        # Execute use case
        post = use_case.execute(use_case_request)
        
        return map_post_to_response(post)
        
    except PostAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[PostResponse])
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    author_id: int = Query(None),
    published_only: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List posts"""
    container = get_container(db)
    use_case = container.list_posts_use_case()
    
    try:
        # If requesting non-published posts, must be same author or admin
        if not published_only:
            if not author_id:
                author_id = current_user.id
            elif author_id != current_user.id and not current_user.can_moderate_posts():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only view your own unpublished posts"
                )
        
        # Map request to use case request
        use_case_request = ListPostsRequest(
            skip=skip,
            limit=limit,
            author_id=author_id,
            published_only=published_only
        )
        
        # Execute use case
        posts = use_case.execute(use_case_request)
        
        return [map_post_to_response(post) for post in posts]
        
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Get a post by ID"""
    container = get_container(db)
    use_case = container.get_post_use_case()
    
    try:
        post = use_case.execute(post_id, increment_views=True)
        return map_post_to_response(post)
        
    except PostNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/by-slug/{slug}", response_model=PostResponse)
def get_post_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get a post by slug"""
    container = get_container(db)
    use_case = container.get_post_by_slug_use_case()
    
    try:
        post = use_case.execute(slug, increment_views=True)
        return map_post_to_response(post)
        
    except PostNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    request: PostUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a post"""
    container = get_container(db)
    use_case = container.update_post_use_case()
    
    try:
        # Map request to use case request
        use_case_request = UpdatePostRequest(
            post_id=post_id,
            title=request.title,
            content=request.content,
            meta_title=request.meta_title,
            meta_description=request.meta_description,
            status=request.status
        )
        
        # Execute use case
        post = use_case.execute(use_case_request, current_user)
        
        return map_post_to_response(post)
        
    except PostNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UnauthorizedPostAccessError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{post_id}", response_model=SuccessResponse)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a post"""
    container = get_container(db)
    use_case = container.delete_post_use_case()
    
    try:
        success = use_case.execute(post_id, current_user)
        
        if success:
            return SuccessResponse(message="Post deleted successfully")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete post"
            )
        
    except PostNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UnauthorizedPostAccessError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.post("/{post_id}/publish", response_model=PostResponse)
def publish_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Publish a post"""
    container = get_container(db)
    use_case = container.publish_post_use_case()
    
    try:
        post = use_case.execute(post_id, current_user)
        return map_post_to_response(post)
        
    except PostNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UnauthorizedPostAccessError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except PostNotPublishableError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )