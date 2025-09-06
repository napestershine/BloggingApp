from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from app.database.connection import get_db
from app.models.models import User
from app.schemas.schemas import (
    UserCreate, User as UserSchema, Token, 
    EmailVerificationRequest, EmailVerificationConfirm,
    PasswordResetRequest, PasswordResetConfirm
)
from app.schemas.responses import SuccessResponse, CreatedResponse
from app.auth.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    get_current_user
)
from app.services.user_service import user_service
from app.utils.security import SecurityValidator
from app.core.config import get_settings
import secrets
import uuid

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=CreatedResponse[UserSchema], status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with enhanced validation"""
    # Validate password strength before creating user
    validation = SecurityValidator.validate_password_strength(user.password)
    if not validation["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation["message"]
        )
    
    # Use the service layer for user creation
    db_user = user_service.create_user(db, user)
    
    return CreatedResponse(
        message="User registered successfully",
        data=db_user
    )

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user with enhanced security"""
    # Use service layer for authentication
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    settings = get_settings()
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-email")
def request_email_verification(
    request: EmailVerificationRequest, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Generate verification token
    verification_token = str(uuid.uuid4())
    user.email_verification_token = verification_token
    
    db.commit()
    
    # In a real app, you would send an email here
    # For now, return the token for testing
    return {
        "message": "Verification email sent",
        "token": verification_token  # Remove this in production
    }

@router.post("/verify-email/confirm")
def confirm_email_verification(
    request: EmailVerificationConfirm,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email_verification_token == request.token
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )
    
    user.email_verified = True
    user.email_verification_token = None
    
    db.commit()
    
    return {"message": "Email verified successfully"}

@router.post("/password/forgot")
def forgot_password(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Don't reveal if user exists or not
        return {"message": "If email exists, password reset link has been sent"}
    
    # Generate reset token
    reset_token = str(uuid.uuid4())
    user.password_reset_token = reset_token
    user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
    
    db.commit()
    
    # In a real app, you would send an email here
    # For now, return the token for testing
    return {
        "message": "Password reset link sent",
        "token": reset_token  # Remove this in production
    }

@router.post("/password/reset")
def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.password_reset_token == request.token
    ).first()
    
    if not user or not user.password_reset_expires:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
    
    if datetime.utcnow() > user.password_reset_expires:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    
    db.commit()
    
    return {"message": "Password reset successfully"}

@router.post("/refresh", response_model=Token)
def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token for authenticated user"""
    settings = get_settings()
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user (client should discard the token)"""
    return {"message": "Successfully logged out"}