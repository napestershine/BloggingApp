"""SQLAlchemy implementation of repository ports"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import User as UserEntity
from app.domain.errors import UserNotFoundError, UserAlreadyExistsError
from app.models.models import User as UserModel
from app.ports.repositories import UserRepository


class SqlAlchemyUserRepository:
    """SQLAlchemy implementation of UserRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: UserEntity) -> UserEntity:
        """Create a new user"""
        # Check for existing user
        if self.get_by_username(user.username):
            raise UserAlreadyExistsError("username", user.username)
        
        if self.get_by_email(user.email):
            raise UserAlreadyExistsError("email", user.email)
        
        # Convert domain entity to SQLAlchemy model
        db_user = UserModel(
            username=user.username,
            email=user.email,
            name=user.name,
            hashed_password="",  # This should be set by use case
            role=user.role,
            email_verified=user.email_verified,
            bio=user.bio,
            avatar_url=user.avatar_url,
            whatsapp_number=user.whatsapp_number,
            whatsapp_notifications_enabled=user.whatsapp_notifications_enabled
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        # Convert back to domain entity
        return self._to_entity(db_user)
    
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        """Get user by ID"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None
    
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        """Get user by username"""
        db_user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(db_user) if db_user else None
    
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email"""
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user) if db_user else None
    
    def update(self, user: UserEntity) -> UserEntity:
        """Update existing user"""
        if not user.id:
            raise ValueError("User ID is required for update")
        
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            raise UserNotFoundError(str(user.id))
        
        # Update fields
        db_user.username = user.username
        db_user.email = user.email
        db_user.name = user.name
        db_user.role = user.role
        db_user.email_verified = user.email_verified
        db_user.bio = user.bio
        db_user.avatar_url = user.avatar_url
        db_user.whatsapp_number = user.whatsapp_number
        db_user.whatsapp_notifications_enabled = user.whatsapp_notifications_enabled
        
        self.db.commit()
        self.db.refresh(db_user)
        
        return self._to_entity(db_user)
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    def _to_entity(self, db_user: UserModel) -> UserEntity:
        """Convert SQLAlchemy model to domain entity"""
        return UserEntity(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            name=db_user.name,
            role=db_user.role,
            created_at=db_user.created_at,
            email_verified=db_user.email_verified,
            bio=db_user.bio,
            avatar_url=db_user.avatar_url,
            whatsapp_number=db_user.whatsapp_number,
            whatsapp_notifications_enabled=db_user.whatsapp_notifications_enabled
        )