"""Service port interfaces using Protocol for type safety"""
from typing import Protocol
from datetime import timedelta


class PasswordHasher(Protocol):
    """Password hashing service interface"""
    
    def hash_password(self, password: str) -> str:
        """Hash a plain text password"""
        ...
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        ...


class TokenService(Protocol):
    """Token generation and validation service interface"""
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """Create access token"""
        ...
    
    def decode_token(self, token: str) -> dict:
        """Decode and validate token"""
        ...
    
    def create_verification_token(self, data: dict) -> str:
        """Create email verification token"""
        ...
    
    def create_reset_token(self, data: dict) -> str:
        """Create password reset token"""
        ...


class SlugGenerator(Protocol):
    """Slug generation service interface"""
    
    def generate_slug(self, text: str) -> str:
        """Generate URL-friendly slug from text"""
        ...
    
    def ensure_unique_slug(self, base_slug: str, existing_slugs: list[str]) -> str:
        """Ensure slug is unique by appending number if needed"""
        ...


class EmailSender(Protocol):
    """Email sending service interface"""
    
    def send_verification_email(self, email: str, token: str) -> bool:
        """Send email verification"""
        ...
    
    def send_password_reset_email(self, email: str, token: str) -> bool:
        """Send password reset email"""
        ...
    
    def send_notification_email(self, email: str, subject: str, content: str) -> bool:
        """Send general notification email"""
        ...