import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.models import Media, User
from app.schemas.schemas import Media as MediaSchema
from app.auth.auth import get_current_user
import aiofiles
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/media", tags=["media"])

# Configuration
UPLOAD_DIR = "/tmp/uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    'images': {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
    'documents': {'.pdf', '.doc', '.docx', '.txt', '.md'}
}
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf', 'application/msword', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain', 'text/markdown'
}

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def validate_file(file: UploadFile) -> tuple[bool, str]:
    """Validate uploaded file"""
    
    # Check file size
    if hasattr(file, 'size') and file.size > MAX_FILE_SIZE:
        return False, f"File size exceeds maximum allowed size of {MAX_FILE_SIZE} bytes"
    
    # Check mime type
    if file.content_type not in ALLOWED_MIME_TYPES:
        return False, f"File type {file.content_type} is not allowed"
    
    # Check file extension
    if file.filename:
        file_ext = os.path.splitext(file.filename)[1].lower()
        all_allowed_extensions = set()
        for extensions in ALLOWED_EXTENSIONS.values():
            all_allowed_extensions.update(extensions)
        
        if file_ext not in all_allowed_extensions:
            return False, f"File extension {file_ext} is not allowed"
    
    return True, ""

@router.post("/upload", response_model=MediaSchema, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a file"""
    
    # Validate file
    is_valid, error_message = validate_file(file)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    try:
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1] if file.filename else ''
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Read file content and get size
        content = await file.read()
        file_size = len(content)
        
        # Additional size check after reading
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size {file_size} exceeds maximum allowed size of {MAX_FILE_SIZE} bytes"
            )
        
        # Save file to disk
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Create media record in database
        db_media = Media(
            filename=unique_filename,
            original_filename=file.filename or "unknown",
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type or "application/octet-stream",
            uploaded_by=current_user.id
        )
        
        db.add(db_media)
        db.commit()
        db.refresh(db_media)
        
        logger.info(f"File uploaded successfully: {unique_filename} by user {current_user.id}")
        return db_media
        
    except Exception as e:
        # Clean up file if database operation fails
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
        
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File upload failed"
        )

@router.get("/{media_id}")
async def get_file(media_id: int, db: Session = Depends(get_db)):
    """Serve uploaded file"""
    
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(media.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(
        path=media.file_path,
        filename=media.original_filename,
        media_type=media.mime_type
    )

@router.get("/", response_model=List[MediaSchema])
def list_media(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user's uploaded media files"""
    media_files = db.query(Media).filter(
        Media.uploaded_by == current_user.id
    ).offset(skip).limit(limit).all()
    return media_files

@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete uploaded media file"""
    
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Only the uploader can delete their files
    if media.uploaded_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this file"
        )
    
    # Delete file from disk
    try:
        if os.path.exists(media.file_path):
            os.remove(media.file_path)
    except OSError as e:
        logger.warning(f"Could not delete file from disk: {media.file_path}, error: {e}")
    
    # Delete record from database
    db.delete(media)
    db.commit()
    
    logger.info(f"Media file deleted: {media.filename} by user {current_user.id}")
    return