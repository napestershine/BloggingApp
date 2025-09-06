from typing import List
from sqlalchemy.orm import Session
from app.models.models import BlogPost
from app.schemas.schemas import SlugValidation, SlugSuggestion
import re
import unicodedata

class SlugService:
    
    def validate_slug(self, db: Session, slug: str, exclude_post_id: int = None) -> SlugValidation:
        """
        Validate if a slug is available and provide suggestions if not
        """
        # Clean the slug
        clean_slug = self._clean_slug(slug)
        
        # Check if slug exists
        query = db.query(BlogPost).filter(BlogPost.slug == clean_slug)
        if exclude_post_id:
            query = query.filter(BlogPost.id != exclude_post_id)
        
        existing_post = query.first()
        is_available = existing_post is None
        
        suggestions = []
        if not is_available:
            suggestions = self._generate_slug_variations(db, clean_slug, exclude_post_id)
        
        return SlugValidation(
            slug=clean_slug,
            is_available=is_available,
            suggestions=suggestions
        )
    
    def suggest_slugs(self, db: Session, title: str) -> SlugSuggestion:
        """
        Generate slug suggestions based on a title
        """
        base_slug = self._clean_slug(title)
        suggestions = [base_slug]
        
        # If base slug is taken, generate variations
        if db.query(BlogPost).filter(BlogPost.slug == base_slug).first():
            suggestions = self._generate_slug_variations(db, base_slug)
        
        # Add alternative slug formats
        alt_slugs = self._generate_alternative_slugs(title)
        for alt_slug in alt_slugs:
            if alt_slug not in suggestions:
                # Check if available
                if not db.query(BlogPost).filter(BlogPost.slug == alt_slug).first():
                    suggestions.append(alt_slug)
        
        return SlugSuggestion(
            title=title,
            suggestions=suggestions[:10]  # Limit to 10 suggestions
        )
    
    def _clean_slug(self, text: str) -> str:
        """
        Clean and normalize text to create a valid slug
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Handle Unicode characters
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        
        # Replace spaces and special characters with hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        
        # Remove leading/trailing hyphens
        text = text.strip('-')
        
        # Limit length
        text = text[:100]
        
        return text
    
    def _generate_slug_variations(self, db: Session, base_slug: str, exclude_post_id: int = None) -> List[str]:
        """
        Generate numbered variations of a slug
        """
        suggestions = []
        
        # Try numbered variations
        for i in range(2, 11):  # Generate up to 10 variations
            variant = f"{base_slug}-{i}"
            query = db.query(BlogPost).filter(BlogPost.slug == variant)
            if exclude_post_id:
                query = query.filter(BlogPost.id != exclude_post_id)
            
            if not query.first():
                suggestions.append(variant)
        
        return suggestions
    
    def _generate_alternative_slugs(self, title: str) -> List[str]:
        """
        Generate alternative slug formats from title
        """
        alternatives = []
        
        if not title:
            return alternatives
        
        words = title.lower().split()
        
        # Different word combinations
        if len(words) > 1:
            # First and last word
            alternatives.append(self._clean_slug(f"{words[0]}-{words[-1]}"))
            
            # First two words
            if len(words) >= 2:
                alternatives.append(self._clean_slug(f"{words[0]}-{words[1]}"))
            
            # Last two words
            if len(words) >= 2:
                alternatives.append(self._clean_slug(f"{words[-2]}-{words[-1]}"))
            
            # Remove common words and join
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
            filtered_words = [w for w in words if w not in common_words]
            if filtered_words and len(filtered_words) != len(words):
                alternatives.append(self._clean_slug('-'.join(filtered_words)))
        
        # Add abbreviated version
        if len(title) > 50:
            abbreviated = ' '.join(words[:5])  # First 5 words
            alternatives.append(self._clean_slug(abbreviated))
        
        return alternatives