"""
User seeder for creating sample users
"""
from .base import BaseSeeder
from app.models.user import User, UserRole
from app.auth.auth import get_password_hash
import logging

logger = logging.getLogger(__name__)


class UserSeeder(BaseSeeder):
    """Seeder for creating sample users"""
    
    def seed(self):
        """Create sample users"""
        users_data = [
            {
                "username": "admin",
                "email": "admin@blogapp.com",
                "name": "Admin User",
                "password": "admin123",
                "role": UserRole.ADMIN,
                "bio": "Site administrator with full privileges.",
                "email_verified": True
            },
            {
                "username": "editor",
                "email": "editor@blogapp.com", 
                "name": "Editor Smith",
                "password": "editor123",
                "role": UserRole.USER,
                "bio": "Content editor and writer.",
                "email_verified": True
            },
            {
                "username": "user1",
                "email": "user1@blogapp.com",
                "name": "John Doe",
                "password": "user123",
                "role": UserRole.USER,
                "bio": "Regular user who loves reading and commenting on blogs.",
                "email_verified": True
            },
            {
                "username": "user2", 
                "email": "user2@blogapp.com",
                "name": "Jane Smith",
                "password": "user123",
                "role": UserRole.USER,
                "bio": "Technology enthusiast and blogger.",
                "email_verified": True
            }
        ]
        
        created_count = 0
        for user_data in users_data:
            password = user_data.pop("password")
            user, created = self.get_or_create(
                User,
                username=user_data["username"],
                defaults={
                    **user_data,
                    "hashed_password": get_password_hash(password)
                }
            )
            if created:
                created_count += 1
                logger.info(f"Created user: {user.username}")
            else:
                logger.info(f"User already exists: {user.username}")
        
        logger.info(f"User seeding completed. Created {created_count} new users.")
    
    def clear(self):
        """Remove seeded users (except admin to avoid breaking system)"""
        seeded_usernames = ["editor", "user1", "user2"]
        deleted_count = 0
        
        for username in seeded_usernames:
            user = self.db.query(User).filter(User.username == username).first()
            if user:
                self.db.delete(user)
                deleted_count += 1
                logger.info(f"Deleted user: {username}")
        
        self.safe_commit()
        logger.info(f"User clearing completed. Deleted {deleted_count} users.")
