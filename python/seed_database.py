#!/usr/bin/env python3
"""
Database seeder script to create initial admin user
"""
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine
from app.models.models import User, UserRole, Base
from app.auth.auth import get_password_hash

def create_admin_user(db: Session):
    """
    Create default admin user if it doesn't exist
    """
    # Check if admin user already exists
    admin_user = db.query(User).filter(User.username == "admin").first()
    
    if admin_user:
        # Update existing admin user's role if needed
        if admin_user.role != UserRole.ADMIN:
            admin_user.role = UserRole.ADMIN
            db.commit()
            print(f"Updated existing user '{admin_user.username}' to admin role")
        else:
            print(f"Admin user '{admin_user.username}' already exists with admin role")
        return admin_user
    
    # Create new admin user
    hashed_password = get_password_hash("admin123")
    admin_user = User(
        username="admin",
        email="admin@blogapp.com",
        name="Admin User",
        hashed_password=hashed_password,
        role=UserRole.ADMIN,
        email_verified=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"Created admin user: {admin_user.username} (ID: {admin_user.id})")
    return admin_user

def seed_database():
    """
    Main seeding function
    """
    print("Starting database seeding...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = create_admin_user(db)
        
        print("\nDatabase seeding completed successfully!")
        print(f"Admin credentials: username='admin', password='admin123'")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()