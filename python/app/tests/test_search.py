import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import User, BlogPost, Category, Tag


class TestSearchEndpoints:
    """Test suite for search functionality."""

    def setup_method(self):
        """Set up test data."""
        pass

    def test_search_posts_empty_query(self, client: TestClient, test_db):
        """Test search with empty query returns 400."""
        response = client.get("/search/")
        assert response.status_code == 422  # Validation error

    def test_search_posts_by_title(self, client: TestClient, test_db):
        """Test searching posts by title."""
        # Create test user
        db = test_db()
        user = User(
            username="testuser",
            email="test@example.com", 
            name="Test User",
            hashed_password="hashed"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create test post
        post = BlogPost(
            title="Python Programming Guide",
            content="A comprehensive guide to Python programming",
            slug="python-programming-guide",
            author_id=user.id
        )
        db.add(post)
        db.commit()
        db.close()

        # Search for the post
        response = client.get("/search/?q=python")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Python Programming Guide"

    def test_search_posts_by_content(self, client: TestClient, test_db):
        """Test searching posts by content."""
        # Create test data
        db = test_db()
        user = User(
            username="testuser",
            email="test@example.com",
            name="Test User", 
            hashed_password="hashed"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        post = BlogPost(
            title="Web Development",
            content="Learn about FastAPI and modern web development practices",
            slug="web-development",
            author_id=user.id
        )
        db.add(post)
        db.commit()
        db.close()

        # Search for content
        response = client.get("/search/?q=FastAPI")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert "FastAPI" in data["results"][0]["content"]

    def test_search_with_category_filter(self, client: TestClient, test_db):
        """Test search with category filter."""
        # Create test data
        db = test_db()
        user = User(
            username="testuser",
            email="test@example.com",
            name="Test User",
            hashed_password="hashed"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        category = Category(
            name="Technology",
            slug="technology",
            created_by=user.id
        )
        db.add(category)
        db.commit()
        db.refresh(category)

        post = BlogPost(
            title="AI and Machine Learning",
            content="Exploring artificial intelligence concepts",
            slug="ai-machine-learning",
            author_id=user.id
        )
        post.categories.append(category)
        db.add(post)
        db.commit()
        db.close()

        # Search with category filter
        response = client.get("/search/?q=AI&category=Technology")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "AI and Machine Learning"

    def test_search_with_author_filter(self, client: TestClient, test_db):
        """Test search with author filter."""
        # Create test data
        db = test_db()
        user = User(
            username="johndoe",
            email="john@example.com",
            name="John Doe",
            hashed_password="hashed"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        post = BlogPost(
            title="Software Engineering Best Practices",
            content="Guidelines for writing maintainable code",
            slug="software-engineering-practices",
            author_id=user.id
        )
        db.add(post)
        db.commit()
        db.close()

        # Search with author filter
        response = client.get("/search/?q=software&author=johndoe")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert data["results"][0]["author_username"] == "johndoe"

    def test_search_suggestions(self, client: TestClient, test_db):
        """Test search suggestions endpoint."""
        # Create test data
        db = test_db()
        user = User(
            username="testuser",
            email="test@example.com",
            name="Test User",
            hashed_password="hashed"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        post = BlogPost(
            title="React Development Tutorial",
            content="Learn React from scratch",
            slug="react-development-tutorial",
            author_id=user.id
        )
        db.add(post)
        db.commit()
        db.close()

        # Test suggestions
        response = client.get("/search/suggestions?q=React")
        assert response.status_code == 200
        data = response.json()
        assert "titles" in data
        assert len(data["titles"]) >= 1
        assert any("React" in title for title in data["titles"])

    def test_search_filters_endpoint(self, client: TestClient, test_db):
        """Test search filters endpoint."""
        # Create test data
        db = test_db()
        user = User(
            username="testuser",
            email="test@example.com",
            name="Test User",
            hashed_password="hashed"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        category = Category(
            name="Technology",
            slug="technology",
            created_by=user.id
        )
        db.add(category)

        tag = Tag(
            name="python",
            created_by=user.id
        )
        db.add(tag)
        db.commit()
        db.close()

        # Test filters endpoint
        response = client.get("/search/filters")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert "tags" in data
        assert "authors" in data
        assert len(data["categories"]) >= 1
        assert len(data["tags"]) >= 1
        assert len(data["authors"]) >= 1

    def test_search_pagination(self, client: TestClient, test_db):
        """Test search results pagination."""
        # Create test data
        db = test_db()
        user = User(
            username="testuser",
            email="test@example.com",
            name="Test User",
            hashed_password="hashed"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create multiple posts
        for i in range(5):
            post = BlogPost(
                title=f"Development Post {i+1}",
                content=f"Content about development topic {i+1}",
                slug=f"development-post-{i+1}",
                author_id=user.id
            )
            db.add(post)
        db.commit()
        db.close()

        # Test pagination
        response = client.get("/search/?q=development&limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 2
        assert data["total"] == 5
        assert data["has_more"] == True

        # Test second page
        response = client.get("/search/?q=development&limit=2&offset=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 2
        assert data["offset"] == 2

    def test_search_no_results(self, client: TestClient, test_db):
        """Test search with no matching results."""
        response = client.get("/search/?q=nonexistentterm12345")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["results"]) == 0
        assert data["has_more"] == False