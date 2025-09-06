"""
Security utilities for input validation and protection
"""
import re
import html
from typing import Any, Dict
from fastapi import HTTPException, status

class SecurityValidator:
    """Utility class for security validations"""
    
    # Common patterns for validation
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,30}$')
    PHONE_PATTERN = re.compile(r'^\+?[1-9]\d{1,14}$')
    
    # Dangerous patterns to check
    DANGEROUS_PATTERNS = [
        re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
        re.compile(r'javascript:', re.IGNORECASE),
        re.compile(r'on\w+\s*=', re.IGNORECASE),
        re.compile(r'eval\s*\(', re.IGNORECASE),
        re.compile(r'expression\s*\(', re.IGNORECASE),
    ]
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validate email format"""
        if not email or len(email) > 254:
            return False
        return bool(cls.EMAIL_PATTERN.match(email))
    
    @classmethod
    def validate_username(cls, username: str) -> bool:
        """Validate username format"""
        if not username:
            return False
        return bool(cls.USERNAME_PATTERN.match(username))
    
    @classmethod
    def validate_phone(cls, phone: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return False
        return bool(cls.PHONE_PATTERN.match(phone.replace(' ', '').replace('-', '')))
    
    @classmethod
    def validate_password_strength(cls, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        if not password:
            return {"valid": False, "message": "Password is required"}
        
        issues = []
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            issues.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            issues.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            issues.append("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("Password must contain at least one special character")
        
        return {
            "valid": len(issues) == 0,
            "message": "; ".join(issues) if issues else "Password is strong"
        }
    
    @classmethod
    def sanitize_input(cls, input_text: str) -> str:
        """Sanitize user input to prevent XSS"""
        if not input_text:
            return input_text
        
        # HTML escape
        sanitized = html.escape(input_text)
        
        # Check for dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            if pattern.search(sanitized):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Input contains potentially dangerous content"
                )
        
        return sanitized
    
    @classmethod
    def validate_file_upload(cls, filename: str, allowed_extensions: set = None) -> bool:
        """Validate file upload"""
        if not filename:
            return False
        
        # Default allowed extensions for images
        if allowed_extensions is None:
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        
        # Get file extension
        extension = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
        
        return extension in allowed_extensions
    
    @classmethod
    def validate_content_length(cls, content: str, max_length: int = 10000) -> bool:
        """Validate content length"""
        return len(content) <= max_length if content else True

def require_valid_email(email: str) -> str:
    """Dependency for email validation"""
    if not SecurityValidator.validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    return email

def require_valid_username(username: str) -> str:
    """Dependency for username validation"""
    if not SecurityValidator.validate_username(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be 3-30 characters long and contain only letters, numbers, and underscores"
        )
    return username

def require_strong_password(password: str) -> str:
    """Dependency for password strength validation"""
    validation = SecurityValidator.validate_password_strength(password)
    if not validation["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation["message"]
        )
    return password