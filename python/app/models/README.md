# Models Refactoring

This directory contains the refactored models for better organization and maintainability.

## Structure

### Before Refactoring
- All models were in a single `models.py` file (264 lines)
- Difficult to navigate and maintain
- Poor separation of concerns

### After Refactoring
Models are now organized into separate files:

- **`user.py`** - User model and UserRole enum
- **`blog_post.py`** - BlogPost model, PostStatus enum, and association tables  
- **`comment.py`** - Comment and CommentReaction models, CommentStatus and ReactionType enums
- **`media.py`** - Media model for file uploads
- **`category.py`** - Category model for post categorization
- **`tag.py`** - Tag model for post tagging
- **`post_engagement.py`** - PostLike and PostShare models, SharingPlatform enum

### Backward Compatibility

- **`models.py`** - Maintains backward compatibility by importing from the new structure
- **`__init__.py`** - Provides direct imports for the new structure
- All existing imports continue to work without changes

## Benefits

1. **Better Organization** - Each model is in its own focused file
2. **Easier Maintenance** - Smaller, more manageable files
3. **Improved Readability** - Related models and enums are grouped together
4. **Backward Compatibility** - No breaking changes to existing code
5. **Better IDE Support** - Easier navigation and autocompletion

## Usage

### New Import Style (Recommended)
```python
from app.models.user import User, UserRole
from app.models.blog_post import BlogPost, PostStatus
```

### Legacy Import Style (Still Supported)
```python
from app.models.models import User, BlogPost
from app.models import User, BlogPost  # Also works
```

Both import styles work and reference the same model classes.