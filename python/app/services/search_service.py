from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, func
from app.models.models import BlogPost, User
from app.schemas.schemas import SearchQuery, SearchResult, SearchSuggestion
import json
import re

class SearchService:
    
    def search_posts(self, db: Session, query: SearchQuery) -> SearchResult:
        """
        Perform full-text search on blog posts with filters and sorting
        """
        # Start with base query
        search_query = db.query(BlogPost).join(User)
        
        # Apply text search if query provided
        if query.q:
            search_terms = query.q.strip().split()
            for term in search_terms:
                search_query = search_query.filter(
                    or_(
                        BlogPost.title.ilike(f"%{term}%"),
                        BlogPost.content.ilike(f"%{term}%"),
                        BlogPost.meta_title.ilike(f"%{term}%"),
                        BlogPost.meta_description.ilike(f"%{term}%"),
                        User.name.ilike(f"%{term}%"),
                        User.username.ilike(f"%{term}%")
                    )
                )
        
        # Apply category filter
        if query.category:
            search_query = search_query.filter(BlogPost.category == query.category)
        
        # Apply author filter
        if query.author:
            search_query = search_query.filter(
                or_(
                    User.username.ilike(f"%{query.author}%"),
                    User.name.ilike(f"%{query.author}%")
                )
            )
        
        # Apply tags filter
        if query.tags:
            for tag in query.tags:
                search_query = search_query.filter(
                    BlogPost.tags.ilike(f"%{tag}%")
                )
        
        # Get total count before pagination
        total = search_query.count()
        
        # Apply sorting
        if query.sort_by == "date":
            search_query = search_query.order_by(desc(BlogPost.published))
        elif query.sort_by == "views":
            search_query = search_query.order_by(desc(BlogPost.view_count))
        elif query.sort_by == "updated":
            search_query = search_query.order_by(desc(BlogPost.updated_at))
        else:  # relevance (default)
            # Simple relevance scoring based on title match preference
            search_query = search_query.order_by(desc(BlogPost.published))
        
        # Apply pagination
        posts = search_query.offset(query.offset).limit(query.limit).all()
        
        # Generate suggestions based on query
        suggestions = self._generate_suggestions(db, query.q) if query.q else []
        
        return SearchResult(
            posts=posts,
            total=total,
            suggestions=suggestions
        )
    
    def get_search_suggestions(self, db: Session, query: str) -> SearchSuggestion:
        """
        Get search suggestions based on partial query
        """
        suggestions = self._generate_suggestions(db, query)
        return SearchSuggestion(query=query, suggestions=suggestions)
    
    def get_search_filters(self, db: Session) -> dict:
        """
        Get available search filters (categories, tags, authors)
        """
        # Get unique categories
        categories = db.query(BlogPost.category).filter(
            BlogPost.category.isnot(None)
        ).distinct().all()
        categories = [cat[0] for cat in categories if cat[0]]
        
        # Get unique authors
        authors = db.query(User.username, User.name).join(BlogPost).distinct().all()
        author_list = [{"username": author[0], "name": author[1]} for author in authors]
        
        # Get unique tags (parse from JSON strings)
        tags_raw = db.query(BlogPost.tags).filter(
            BlogPost.tags.isnot(None)
        ).all()
        
        all_tags = set()
        for tag_row in tags_raw:
            if tag_row[0]:
                try:
                    tags = json.loads(tag_row[0])
                    if isinstance(tags, list):
                        all_tags.update(tags)
                    elif isinstance(tags, str):
                        # Handle comma-separated tags
                        all_tags.update([t.strip() for t in tags.split(",")])
                except (json.JSONDecodeError, AttributeError):
                    # Handle plain text tags
                    if isinstance(tag_row[0], str):
                        all_tags.update([t.strip() for t in tag_row[0].split(",")])
        
        return {
            "categories": categories,
            "authors": author_list,
            "tags": list(all_tags)
        }
    
    def _generate_suggestions(self, db: Session, query: str) -> List[str]:
        """
        Generate search suggestions based on existing content
        """
        if not query or len(query) < 2:
            return []
        
        suggestions = []
        
        # Get title suggestions
        title_matches = db.query(BlogPost.title).filter(
            BlogPost.title.ilike(f"%{query}%")
        ).limit(5).all()
        
        for match in title_matches:
            title = match[0]
            # Extract words that contain the query
            words = re.findall(r'\b\w*' + re.escape(query.lower()) + r'\w*\b', title.lower())
            suggestions.extend(words)
        
        # Get category suggestions
        category_matches = db.query(BlogPost.category).filter(
            BlogPost.category.ilike(f"%{query}%")
        ).distinct().limit(3).all()
        
        suggestions.extend([cat[0] for cat in category_matches if cat[0]])
        
        # Remove duplicates and return limited results
        return list(set(suggestions))[:10]