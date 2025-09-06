"""
User service with improved business logic and database operations
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate
from app.services.base_service import BaseService
from app.auth.auth import get_password_hash, verify_password

class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Enhanced user service with business logic"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def create_user(self, db: Session, user_create: UserCreate) -> User:
        """Create new user with password validation"""
        # Check if passwords match
        if user_create.password != user_create.retyped_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        
        # Check if user already exists
        if self.get_by_username(db, user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if self.get_by_email(db, user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user with hashed password
        user_data = user_create.model_dump()
        user_data.pop('retyped_password')  # Remove confirmation password
        user_data['hashed_password'] = get_password_hash(user_data.pop('password'))
        
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = self.get_by_username(db, username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def update_password(self, db: Session, user: User, new_password: str) -> User:
        """Update user password"""
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
        return user
    
    def search_users(
        self, 
        db: Session, 
        query: str, 
        skip: int = 0, 
        limit: int = 20
    ) -> list[User]:
        """Search users by username or name"""
        return (
            db.query(User)
            .filter(
                (User.username.ilike(f"%{query}%")) |
                (User.name.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

# Global user service instance
user_service = UserService()