# SEO & Discovery Features Guide

This guide covers the newly implemented SEO and Discovery features for the BloggingApp API.

## 🔍 Search Features

### Advanced Search
```http
GET /api/search/?q=python&category=technology&sort_by=views&limit=10
```

**Parameters:**
- `q` (required): Search query
- `category` (optional): Filter by category
- `tags` (optional): Filter by tags (can specify multiple)
- `author` (optional): Filter by author name/username
- `sort_by` (optional): Sort by `relevance`, `date`, `views`, or `updated`
- `limit` (optional): Number of results (1-100, default: 10)
- `offset` (optional): Pagination offset (default: 0)

### Search Suggestions
```http
GET /api/search/suggestions?q=pyth
```

### Available Filters
```http
GET /api/search/filters
```
Returns available categories, authors, and tags for filtering.

## 🎯 SEO Management

### Get Post SEO Data
```http
GET /api/seo/posts/{post_id}
```

### Update Post SEO Data
```http
PUT /api/seo/posts/{post_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "meta_title": "Custom Meta Title",
  "meta_description": "Custom meta description for SEO",
  "og_title": "Open Graph Title",
  "og_description": "Open Graph description for social sharing",
  "og_image": "https://example.com/image.jpg"
}
```

### SEO Preview
```http
GET /api/seo/posts/{post_id}/preview?base_url=https://myblog.com
```

### SEO Validation
```http
POST /api/seo/validate
Content-Type: application/json

{
  "meta_title": "Title to validate",
  "meta_description": "Description to validate"
}
```

## 🗺️ Sitemap & SEO Tools

### XML Sitemap
```http
GET /api/sitemap.xml?base_url=https://myblog.com
```

### Sitemap Data (JSON)
```http
GET /api/sitemap/posts
```

### Robots.txt
```http
GET /api/robots.txt?base_url=https://myblog.com
```

## 🔗 URL Slug Management

### Validate Slug
```http
GET /api/slugs/validate?slug=my-post-slug&exclude_post_id=123
```

### Generate Slug Suggestions
```http
GET /api/slugs/suggest?title=How to Learn Programming
```

## 📈 Content Discovery

### Trending Posts
```http
GET /api/posts/trending?limit=10&days=7
```

### Hot Topics
```http
GET /api/topics/hot?limit=10
```

### Related Posts
```http
GET /api/posts/{post_id}/related?limit=5
```

## 🎪 Personalized Feeds

### Personalized Feed (Authentication Required)
```http
GET /api/feed/personalized?limit=10&offset=0
Authorization: Bearer <token>
```

### User Interests (Authentication Required)
```http
GET /api/feed/user/interests
Authorization: Bearer <token>
```

### Update User Interests (Authentication Required)
```http
PUT /api/feed/user/interests
Authorization: Bearer <token>
Content-Type: application/json

{
  "categories": ["technology", "programming"],
  "tags": ["python", "javascript"],
  "preferred_authors": ["john_doe"],
  "reading_frequency": "daily"
}
```

## 📡 RSS Feeds

### Main RSS Feed
```http
GET /api/rss/?base_url=https://myblog.com&limit=20
```

### Category RSS Feed
```http
GET /api/rss/categories/technology?base_url=https://myblog.com
```

### Author RSS Feed
```http
GET /api/rss/authors/john_doe?base_url=https://myblog.com
```

## 📝 Enhanced Blog Post Creation

Blog posts now support additional SEO fields:

```http
POST /blog_posts/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "How to Learn Python",
  "content": "Python is a great programming language...",
  "slug": "how-to-learn-python",
  "category": "technology",
  "tags": "[\"python\", \"programming\", \"tutorial\"]",
  "meta_title": "Learn Python Programming - Complete Guide",
  "meta_description": "Comprehensive guide to learning Python...",
  "og_title": "Python Programming Guide",
  "og_description": "Master Python with our tutorials",
  "og_image": "https://example.com/python-image.jpg"
}
```

## 🔧 Database Schema Updates

The BlogPost model now includes:
- `meta_title`: Custom meta title for SEO
- `meta_description`: Custom meta description for SEO
- `og_title`: Open Graph title for social sharing
- `og_description`: Open Graph description for social sharing
- `og_image`: Open Graph image URL for social sharing
- `view_count`: Track post popularity
- `updated_at`: Track last modification time
- `tags`: JSON string of post tags
- `category`: Post category

## 📊 Analytics Integration

- View tracking: Posts automatically track view counts when accessed
- Trending algorithm: Based on view counts and recency
- Related posts: Uses category and tag similarity
- Hot topics: Analyzes category and tag frequency with engagement

## 🔒 Authentication

Some endpoints require authentication:
- SEO data updates
- Personalized feeds
- User interest management

Use the existing authentication system with Bearer tokens:
```http
Authorization: Bearer <your_jwt_token>
```

## 🧪 Testing

All features are covered by comprehensive tests. Run the test suite:

```bash
cd python
pytest app/tests/ -v
```

## 📱 Integration Examples

### Frontend Search Implementation
```javascript
// Search with filters
const searchResults = await fetch('/api/search/?q=python&category=technology&sort_by=views');
const data = await searchResults.json();

// Get search suggestions
const suggestions = await fetch('/api/search/suggestions?q=pyth');
const suggestionData = await suggestions.json();
```

### SEO Meta Tags in HTML
```html
<!-- Use the SEO preview data -->
<meta name="title" content="{meta_title || title}">
<meta name="description" content="{meta_description}">
<meta property="og:title" content="{og_title || meta_title || title}">
<meta property="og:description" content="{og_description || meta_description}">
<meta property="og:image" content="{og_image}">
```

### RSS Feed Integration
```html
<!-- Add to HTML head -->
<link rel="alternate" type="application/rss+xml" title="Blog RSS Feed" href="/api/rss/">
<link rel="alternate" type="application/rss+xml" title="Technology Posts" href="/api/rss/categories/technology">
```

This implementation provides a solid foundation for SEO optimization and content discovery, making your blog more discoverable and engaging for users.