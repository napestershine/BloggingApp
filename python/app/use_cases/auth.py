"""Authentication use cases"""
from dataclasses import dataclass
from typing import Optional
from datetime import timedelta

from app.domain.entities import User, UserRole
from app.domain.errors import (
    UserAlreadyExistsError, 
    InvalidCredentialsError,
    WeakPasswordError,
    UserNotFoundError
)
from app.ports.repositories import UserRepository
from app.ports.services import PasswordHasher, TokenService


@dataclass
class RegisterUserRequest:
    username: str
    email: str
    name: str
    password: str
    retyped_password: str


@dataclass
class LoginRequest:
    username: str
    password: str


@dataclass
class AuthResponse:
    user: User
    access_token: str
    token_type: str = "bearer"


class RegisterUserUseCase:
    """Use case for user registration"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
    
    def execute(self, request: RegisterUserRequest) -> AuthResponse:
        """Register a new user"""
        # Validate passwords match
        if request.password != request.retyped_password:
            raise WeakPasswordError("Passwords do not match")
        
        # Validate password strength (basic validation)
        if len(request.password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters long")
        
        # Check if user already exists
        if self.user_repository.get_by_username(request.username):
            raise UserAlreadyExistsError("username", request.username)
        
        if self.user_repository.get_by_email(request.email):
            raise UserAlreadyExistsError("email", request.email)
        
        # Create user entity
        user = User(
            id=None,
            username=request.username,
            email=request.email,
            name=request.name,
            role=UserRole.USER,
            email_verified=False
        )
        
        # Hash password and save user
        hashed_password = self.password_hasher.hash_password(request.password)
        created_user = self.user_repository.create(user, hashed_password)
        
        # Generate access token
        token_data = {"sub": created_user.username, "user_id": created_user.id}
        access_token = self.token_service.create_access_token(token_data)
        
        return AuthResponse(
            user=created_user,
            access_token=access_token
        )


class LoginUserUseCase:
    """Use case for user login"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
    
    def execute(self, request: LoginRequest) -> AuthResponse:
        """Authenticate user and return token"""
        # Find user by username or email
        user = self.user_repository.get_by_username(request.username)
        if not user:
            user = self.user_repository.get_by_email(request.username)
        
        if not user:
            raise InvalidCredentialsError()
        
        # Get hashed password and verify
        hashed_password = self.user_repository.get_hashed_password(request.username)
        if not hashed_password or not self.password_hasher.verify_password(
            request.password, hashed_password
        ):
            raise InvalidCredentialsError()
        
        # Generate access token
        token_data = {"sub": user.username, "user_id": user.id}
        access_token = self.token_service.create_access_token(token_data)
        
        return AuthResponse(
            user=user,
            access_token=access_token
        )


class GetUserByTokenUseCase:
    """Use case for getting user from token"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        token_service: TokenService
    ):
        self.user_repository = user_repository
        self.token_service = token_service
    
    def execute(self, token: str) -> User:
        """Get user from access token"""
        try:
            payload = self.token_service.decode_token(token)
            user_id = payload.get("user_id")
            
            if not user_id:
                raise InvalidCredentialsError()
            
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(str(user_id))
            
            return user
            
        except ValueError:
            raise InvalidCredentialsError()