#!/usr/bin/env python3
"""
Sample Credentials Setup Script

This script creates sample users for testing the BloggingApp functionality.
Run this script to populate the database with test credentials.

Usage:
    python sample_credentials.py

Sample Credentials Created:
- admin@example.com / admin123 (Admin User)
- john@example.com / john123 (John Doe - Regular User)
- jane@example.com / jane123 (Jane Smith - Regular User)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database.connection import get_db, engine
from app.models.models import User, Base
from app.auth.auth import get_password_hash
import json

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_sample_users():
    """Create sample users for testing"""
    db = next(get_db())
    
    sample_users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "name": "Admin User",
            "password": "admin123",
            "bio": "System administrator and content manager",
            "email_verified": True,
            "social_links": {
                "github": "https://github.com/admin",
                "twitter": "@admin",
                "linkedin": "https://linkedin.com/in/admin"
            }
        },
        {
            "username": "johndoe",
            "email": "john@example.com", 
            "name": "John Doe",
            "password": "john123",
            "bio": "Software developer and tech enthusiast. Love writing about programming and technology trends.",
            "email_verified": True,
            "social_links": {
                "github": "https://github.com/johndoe",
                "twitter": "@johndoe",
                "website": "https://johndoe.dev"
            }
        },
        {
            "username": "janesmith",
            "email": "jane@example.com",
            "name": "Jane Smith", 
            "password": "jane123",
            "bio": "UX Designer and blogger. Passionate about creating user-friendly experiences and design systems.",
            "email_verified": True,
            "social_links": {
                "dribbble": "https://dribbble.com/janesmith",
                "twitter": "@janesmith_ux",
                "portfolio": "https://janesmith.design"
            }
        },
        {
            "username": "testuser",
            "email": "test@example.com",
            "name": "Test User",
            "password": "test123",
            "bio": "Test account for development and demo purposes.",
            "email_verified": False,
            "social_links": {}
        }
    ]
    
    created_users = []
    
    for user_data in sample_users:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == user_data["username"]) | (User.email == user_data["email"])
        ).first()
        
        if existing_user:
            print(f"User '{user_data['username']}' already exists, skipping...")
            created_users.append({
                "username": existing_user.username,
                "email": existing_user.email,
                "password": user_data["password"],  # Show the expected password
                "status": "existing"
            })
            continue
            
        # Create new user
        hashed_password = get_password_hash(user_data["password"])
        social_links_json = json.dumps(user_data["social_links"]) if user_data["social_links"] else None
        
        db_user = User(
            username=user_data["username"],
            email=user_data["email"],
            name=user_data["name"],
            hashed_password=hashed_password,
            bio=user_data["bio"],
            email_verified=user_data["email_verified"],
            social_links=social_links_json
        )
        
        db.add(db_user)
        
        created_users.append({
            "username": user_data["username"],
            "email": user_data["email"],
            "password": user_data["password"],
            "status": "created"
        })
        
        print(f"Created user: {user_data['username']} ({user_data['email']})")
    
    db.commit()
    db.close()
    
    return created_users

def display_credentials(users):
    """Display the sample credentials in a nice format"""
    print("\n" + "="*60)
    print("SAMPLE CREDENTIALS FOR BLOGGINGAPP")
    print("="*60)
    print("Use these credentials to test the application:\n")
    
    for user in users:
        status_emoji = "✅" if user["status"] == "created" else "ℹ️"
        print(f"{status_emoji} Username: {user['username']}")
        print(f"   Email:    {user['email']}")
        print(f"   Password: {user['password']}")
        print(f"   Status:   {user['status']}")
        print()
    
    print("API Endpoints to test:")
    print("- POST /auth/register (create new users)")
    print("- POST /auth/login (get access token)")
    print("- POST /auth/verify-email (request email verification)")
    print("- POST /auth/verify-email/confirm (confirm email)")
    print("- POST /auth/password/forgot (password reset request)")
    print("- POST /auth/password/reset (reset password)")
    print("- POST /auth/refresh (refresh access token)")
    print("- POST /auth/logout (logout user)")
    print("- GET /users/{user_id}/profile (get user profile)")
    print("- PUT /users/{user_id}/profile (update user profile)")
    print("- POST /users/upload/avatar (upload avatar)")
    print("\nExample API usage:")
    print('curl -X POST "http://localhost:8000/auth/login" \\')
    print('     -H "Content-Type: application/x-www-form-urlencoded" \\')
    print('     -d "username=admin&password=admin123"')
    print("\n" + "="*60)

if __name__ == "__main__":
    print("Creating sample users for BloggingApp...")
    users = create_sample_users()
    display_credentials(users)