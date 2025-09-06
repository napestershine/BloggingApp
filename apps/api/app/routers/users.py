from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.models import User
from app.schemas.schemas import (
    User as UserSchema, UserUpdate, UserProfile, UserProfileUpdate
)
from app.auth.auth import get_current_user
import json
import os

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Users can only update their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        from app.auth.auth import get_password_hash
        user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}/profile", response_model=UserProfile)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Parse social_links JSON if it exists
    social_links = None
    if user.social_links:
        try:
            social_links = json.loads(user.social_links)
        except json.JSONDecodeError:
            social_links = None
    
    return UserProfile(
        id=user.id,
        username=user.username,
        name=user.name,
        email=user.email,
        bio=user.bio,
        avatar_url=user.avatar_url,
        social_links=social_links,
        created_at=user.created_at
    )

@router.put("/{user_id}/profile", response_model=UserProfile)
def update_user_profile(
    user_id: int,
    profile_update: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Users can only update their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this profile"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided
    if profile_update.name is not None:
        user.name = profile_update.name
    if profile_update.bio is not None:
        user.bio = profile_update.bio
    if profile_update.social_links is not None:
        user.social_links = json.dumps(profile_update.social_links)
    
    db.commit()
    db.refresh(user)
    
    # Parse social_links for response
    social_links = None
    if user.social_links:
        try:
            social_links = json.loads(user.social_links)
        except json.JSONDecodeError:
            social_links = None
    
    return UserProfile(
        id=user.id,
        username=user.username,
        name=user.name,
        email=user.email,
        bio=user.bio,
        avatar_url=user.avatar_url,
        social_links=social_links,
        created_at=user.created_at
    )

@router.post("/upload/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Create upload directory if it doesn't exist
    upload_dir = "uploads/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate filename
    file_extension = file.filename.split('.')[-1] if file.filename else 'jpg'
    filename = f"avatar_{current_user.id}.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Update user avatar_url
    avatar_url = f"/uploads/avatars/{filename}"
    current_user.avatar_url = avatar_url
    
    db.commit()
    
    return {"avatar_url": avatar_url}