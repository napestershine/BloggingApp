# Content Management Tasks (FastAPI + Flutter)

## Task 9: Basic Post CRUD Completion
- **Priority**: P0  
- **Status**: 🚧 PARTIAL (missing delete)
- **Description**: Complete basic blog post operations
- **FastAPI Requirements**:
  - ✅ `GET /blog_posts/` (implemented)
  - ✅ `POST /blog_posts/` (implemented)  
  - ✅ `PUT /blog_posts/{id}` (implemented)
  - ❌ `DELETE /blog_posts/{id}` (missing)
- **Flutter Integration**: Post list, create/edit forms, delete confirmation
- **Estimated Time**: 2 hours (FastAPI) + 1 hour (Flutter)

## Task 10: Media Upload System
- **Priority**: P0
- **Status**: ❌ TODO
- **Description**: File upload for images and documents
- **FastAPI Requirements**:
  - ❌ `POST /media/upload` - Upload files
  - ❌ `GET /media/{id}` - Serve uploaded files
  - ❌ File validation and storage
- **Flutter Integration**: Image picker, file upload with progress, image display
- **Estimated Time**: 6 hours (FastAPI) + 4 hours (Flutter)

## Task 11: Categories & Tags System  
- **Priority**: P1
- **Status**: ❌ TODO
- **Description**: Content organization with categories and tags
- **FastAPI Requirements**:
  - ❌ `GET /categories` - List categories
  - ❌ `POST /categories` - Create category
  - ❌ `GET /tags` - List tags
  - ❌ `POST /tags` - Create tag
  - ❌ `GET /blog_posts/{id}/tags` - Get post tags
  - ❌ `PUT /blog_posts/{id}/tags` - Update post tags
- **Flutter Integration**: Category selection, tag input with autocomplete
- **Estimated Time**: 8 hours (FastAPI) + 4 hours (Flutter)

## Task 12: Draft Management
- **Priority**: P1
- **Status**: ❌ TODO 
- **Description**: Save posts as drafts with auto-save
- **FastAPI Requirements**:
  - ❌ `GET /blog_posts/drafts` - List user drafts
  - ❌ `POST /blog_posts/{id}/autosave` - Auto-save draft
  - ❌ Add `status` field to blog posts (draft/published)
- **Flutter Integration**: Draft indicator, auto-save timer, draft list screen
- **Estimated Time**: 4 hours (FastAPI) + 4 hours (Flutter)

## Task 13: Rich Text Editor Support
- **Priority**: P1
- **Status**: ❌ TODO
- **Description**: Support rich text formatting in posts
- **FastAPI Requirements**:
  - ❌ `POST /blog_posts/preview` - Preview formatted content
  - ❌ Content validation for HTML/Markdown
  - ❌ XSS protection for user content
- **Flutter Integration**: Rich text editor widget, formatting toolbar, preview mode
- **Estimated Time**: 4 hours (FastAPI) + 12 hours (Flutter)

## Task 14: Content Search
- **Priority**: P1
- **Status**: ❌ TODO
- **Description**: Search posts by title, content, tags, categories
- **FastAPI Requirements**:
  - ❌ `GET /search` - Search posts with filters
  - ❌ `GET /search/suggestions` - Autocomplete suggestions
  - ❌ Full-text search implementation
- **Flutter Integration**: Search bar, filters, search results, recent searches
- **Estimated Time**: 8 hours (FastAPI) + 6 hours (Flutter)

## Task 15: Post Scheduling (P2 Priority)
- **Priority**: P2
- **Status**: ❌ TODO
- **Description**: Schedule posts for future publication
- **FastAPI Requirements**:
  - ❌ `POST /blog_posts/schedule` - Schedule post
  - ❌ `GET /blog_posts/scheduled` - List scheduled posts
  - ❌ Background task for publishing scheduled posts
- **Flutter Integration**: Date/time picker, scheduled posts list
- **Estimated Time**: 6 hours (FastAPI) + 4 hours (Flutter)

## Task 16: Version History (P2 Priority)
- **Priority**: P2
- **Status**: ❌ TODO
- **Description**: Track post revisions and enable rollback
- **FastAPI Requirements**:
  - ❌ `GET /blog_posts/{id}/revisions` - Get revision history
  - ❌ `POST /blog_posts/{id}/restore` - Restore revision
  - ❌ Database schema for revision tracking
- **Flutter Integration**: Revision history screen, diff viewer, restore confirmation
- **Estimated Time**: 8 hours (FastAPI) + 6 hours (Flutter)

## Implementation Priority Order

### Phase 1: Core Content Management (P0-P1)
1. Complete post CRUD (delete endpoint)
2. Media upload system  
3. Categories and tags
4. Draft management
5. Basic search functionality

### Phase 2: Enhanced Features (P1-P2)  
6. Rich text editor support
7. Content preview
8. Post scheduling
9. Version history

### Testing Strategy
- **API Testing**: Test file uploads, search functionality, content validation
- **Flutter Testing**: Widget tests for forms, integration tests for upload flow
- **Manual Testing**: Full content creation workflow from draft to publish