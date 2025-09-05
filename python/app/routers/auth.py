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
from app.auth.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    get_current_user
)
from app.core.config import settings
import secrets
import uuid

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if passwords match
    if user.password != user.retyped_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
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