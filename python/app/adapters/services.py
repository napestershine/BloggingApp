"""Service adapters implementing port interfaces"""
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import re
import secrets
from app.ports.services import PasswordHasher, TokenService, SlugGenerator
from app.core.config import settings


class BcryptPasswordHasher:
    """Bcrypt implementation of PasswordHasher"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """Hash a plain text password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)


class JWTTokenService:
    """JWT implementation of TokenService"""
    
    def __init__(self):
        self.secret_key = settings.secret_key.get_secret_value()
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """Create access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> dict:
        """Decode and validate token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise ValueError("Invalid token")
    
    def create_verification_token(self, data: dict) -> str:
        """Create email verification token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=24)  # 24 hour expiry
        to_encode.update({"exp": expire, "type": "email_verification"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_reset_token(self, data: dict) -> str:
        """Create password reset token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
        to_encode.update({"exp": expire, "type": "password_reset"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)


class DefaultSlugGenerator:
    """Default implementation of SlugGenerator"""
    
    def generate_slug(self, text: str) -> str:
        """Generate URL-friendly slug from text"""
        # Convert to lowercase and replace spaces with hyphens
        slug = text.lower().strip()
        # Remove special characters except hyphens
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        # Replace spaces and multiple hyphens with single hyphen
        slug = re.sub(r'[\s-]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug
    
    def ensure_unique_slug(self, base_slug: str, existing_slugs: list[str]) -> str:
        """Ensure slug is unique by appending number if needed"""
        if base_slug not in existing_slugs:
            return base_slug
        
        counter = 1
        while f"{base_slug}-{counter}" in existing_slugs:
            counter += 1
        
        return f"{base_slug}-{counter}"


class MockEmailSender:
    """Mock email sender for development/testing"""
    
    def send_verification_email(self, email: str, token: str) -> bool:
        """Send email verification"""
        print(f"Mock: Sending verification email to {email} with token {token}")
        return True
    
    def send_password_reset_email(self, email: str, token: str) -> bool:
        """Send password reset email"""
        print(f"Mock: Sending password reset email to {email} with token {token}")
        return True
    
    def send_notification_email(self, email: str, subject: str, content: str) -> bool:
        """Send general notification email"""
        print(f"Mock: Sending notification email to {email}, subject: {subject}")
        return True