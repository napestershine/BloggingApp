"""Authentication router using SOLID architecture"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.config.container import get_container, Container
from app.presentation.schemas import (
    UserCreateRequest, UserResponse, LoginRequest, TokenResponse, 
    SuccessResponse, ErrorResponse
)
from app.use_cases.auth import RegisterUserRequest, LoginRequest as LoginUseCaseRequest
from app.domain.errors import (
    UserAlreadyExistsError, InvalidCredentialsError, WeakPasswordError, 
    UserNotFoundError, DomainError
)
from app.domain.entities import User

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def map_user_to_response(user: User) -> UserResponse:
    """Map domain user entity to response schema"""
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        name=user.name,
        role=user.role,
        created_at=user.created_at,
        email_verified=user.email_verified,
        bio=user.bio,
        avatar_url=user.avatar_url
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from token using use case"""
    container = get_container(db)
    use_case = container.get_user_by_token_use_case()
    
    try:
        return use_case.execute(token)
    except (InvalidCredentialsError, UserNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: UserCreateRequest,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    container = get_container(db)
    use_case = container.register_user_use_case()
    
    try:
        # Map request to use case request
        use_case_request = RegisterUserRequest(
            username=request.username,
            email=request.email,
            name=request.name,
            password=request.password,
            retyped_password=request.retyped_password
        )
        
        # Execute use case
        auth_response = use_case.execute(use_case_request)
        
        # Map to response
        return TokenResponse(
            access_token=auth_response.access_token,
            token_type=auth_response.token_type,
            user=map_user_to_response(auth_response.user)
        )
        
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login user"""
    container = get_container(db)
    use_case = container.login_user_use_case()
    
    try:
        # Map request to use case request
        use_case_request = LoginUseCaseRequest(
            username=form_data.username,
            password=form_data.password
        )
        
        # Execute use case
        auth_response = use_case.execute(use_case_request)
        
        # Map to response
        return TokenResponse(
            access_token=auth_response.access_token,
            token_type=auth_response.token_type,
            user=map_user_to_response(auth_response.user)
        )
        
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return map_user_to_response(current_user)