from functools import wraps
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models.models import User, UserRole
from app.database.connection import get_db
from app.auth.auth import get_current_user
from typing import List, Optional

security = HTTPBearer()

def require_admin_role(allowed_roles: List[UserRole] = [UserRole.ADMIN, UserRole.SUPER_ADMIN]):
    """
    Dependency to check if current user has admin privileges
    """
    def check_admin(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required"
            )
        return current_user
    return check_admin

def require_super_admin():
    """
    Dependency to check if current user has super admin privileges
    """
    return require_admin_role([UserRole.SUPER_ADMIN])

def is_admin(user: User) -> bool:
    """
    Check if user has admin privileges
    """
    return user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]

def is_super_admin(user: User) -> bool:
    """
    Check if user has super admin privileges
    """
    return user.role == UserRole.SUPER_ADMIN

def admin_only(func):
    """
    Decorator to protect admin-only functions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = kwargs.get('current_user')
        if not current_user or not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required"
            )
        return func(*args, **kwargs)
    return wrapper

def super_admin_only(func):
    """
    Decorator to protect super admin-only functions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = kwargs.get('current_user')
        if not current_user or not is_super_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Super admin privileges required"
            )
        return func(*args, **kwargs)
    return wrapper