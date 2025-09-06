# Phase 2: Core Admin Features (Week 3-4)

## Task B1: User Management Dashboard
- **Priority**: P0 (Critical)
- **Estimated Time**: 12 hours
- **Status**: TODO
- **Based on**: Task 56 from original admin features

**Frontend Requirements:**
- User list with search, filter, and pagination
- User detail view with profile information
- Edit user form with role assignment
- User status management (active/suspended)
- Bulk user operations

**Backend Requirements:**
- Admin user management API endpoints
- User statistics and analytics
- Role assignment functionality
- User activity logging

**API Endpoints:**
```
GET    /api/admin/users              # Paginated user list with filters
GET    /api/admin/users/{id}         # Get user details
PUT    /api/admin/users/{id}         # Update user (profile, role, status)
DELETE /api/admin/users/{id}         # Soft delete/suspend user
POST   /api/admin/users/{id}/roles   # Assign/update user roles
GET    /api/admin/users/stats        # User statistics
POST   /api/admin/users/bulk         # Bulk user operations
GET    /api/admin/users/activity     # User activity logs
```

**Next.js Pages:**
```
/admin/users                         # User list with table
/admin/users/[id]                    # User profile view
/admin/users/[id]/edit               # Edit user form
/admin/users/new                     # Create admin user
/admin/users/activity                # User activity dashboard
```

**Components:**
```
/src/components/admin/users/
├── UserTable.tsx                    # Sortable user table
├── UserFilters.tsx                  # Search and filter controls  
├── UserCard.tsx                     # User profile card
├── UserEditForm.tsx                 # User editing form
├── UserStats.tsx                    # User statistics widgets
├── UserActivityLog.tsx              # Activity timeline
└── BulkUserActions.tsx              # Bulk operation controls
```

**Features:**
- Search users by name, email, username
- Filter by role, status, registration date
- Sort by various columns
- Export user data to CSV
- User engagement metrics
- Account status indicators

**Dependencies**: Phase 1 (Admin foundation)

---

## Task B2: Content Moderation Dashboard  
- **Priority**: P0 (Critical)
- **Estimated Time**: 14 hours
- **Status**: TODO
- **Based on**: Task 55 from original admin features

**Frontend Requirements:**
- Post moderation queue with approval workflow
- Content review interface with preview
- Batch approval/rejection tools
- Content flagging and reporting system
- Publication scheduling controls

**Backend Requirements:**
- Post moderation API endpoints
- Content approval workflow
- Automated content filtering
- Publishing controls

**API Endpoints:**
```
GET    /api/admin/posts              # All posts with moderation status
GET    /api/admin/posts/pending      # Posts awaiting moderation
GET    /api/admin/posts/reported     # Reported posts
PUT    /api/admin/posts/{id}/status  # Approve/reject/schedule posts
DELETE /api/admin/posts/{id}         # Delete posts
POST   /api/admin/posts/bulk         # Bulk post operations
GET    /api/admin/posts/stats        # Content statistics
POST   /api/admin/posts/{id}/feature # Feature/unfeature posts
```

**Database Changes:**
```sql
-- Add moderation fields to blog_posts table
ALTER TABLE blog_posts ADD COLUMN status VARCHAR(20) DEFAULT 'draft';
ALTER TABLE blog_posts ADD COLUMN featured BOOLEAN DEFAULT FALSE;
ALTER TABLE blog_posts ADD COLUMN moderated_by INTEGER;
ALTER TABLE blog_posts ADD COLUMN moderated_at TIMESTAMP;
ALTER TABLE blog_posts ADD COLUMN rejection_reason TEXT;
```

**Next.js Pages:**
```
/admin/posts                         # All posts dashboard
/admin/posts/pending                 # Moderation queue
/admin/posts/reported                # Reported content
/admin/posts/[id]                    # Post review interface
/admin/posts/[id]/edit               # Admin post editing
/admin/posts/scheduled               # Scheduled posts
```

**Components:**
```
/src/components/admin/posts/
├── PostModerationQueue.tsx          # Pending posts table
├── PostReviewCard.tsx               # Post preview for review
├── PostStatusBadge.tsx              # Status indicator
├── PostModerationForm.tsx           # Approve/reject form
├── PostBulkActions.tsx              # Batch operations
├── PostPreview.tsx                  # Full post preview
├── PostScheduler.tsx                # Publication scheduling
└── PostStats.tsx                    # Content analytics
```

**Moderation Workflow:**
1. **Draft** → **Pending** (author submits)
2. **Pending** → **Approved** (admin approves)
3. **Pending** → **Rejected** (admin rejects with reason)
4. **Approved** → **Published** (scheduled or immediate)
5. **Published** → **Featured** (admin can feature)

**Dependencies**: Phase 1 (Admin foundation)

---

## Task B3: Comment Moderation Tools
- **Priority**: P1 (High)  
- **Estimated Time**: 8 hours
- **Status**: TODO
- **Based on**: Task 57 from original admin features

**Frontend Requirements:**
- Comment review interface
- Bulk comment moderation
- User comment history
- Automated spam detection indicators
- Comment thread context view

**Backend Requirements:**
- Comment moderation API
- Spam detection integration
- Comment approval workflow
- User commenting analytics

**API Endpoints:**
```
GET    /api/admin/comments           # All comments with filters
GET    /api/admin/comments/pending   # Comments awaiting moderation
GET    /api/admin/comments/reported  # Reported comments
PUT    /api/admin/comments/{id}/status # Approve/reject comments
DELETE /api/admin/comments/{id}      # Delete comments
POST   /api/admin/comments/bulk      # Bulk comment operations
GET    /api/admin/comments/spam      # Spam detection queue
GET    /api/admin/comments/user/{id} # User's comment history
```

**Database Changes:**
```sql
-- Add moderation fields to comments table  
ALTER TABLE comments ADD COLUMN status VARCHAR(20) DEFAULT 'approved';
ALTER TABLE comments ADD COLUMN is_spam BOOLEAN DEFAULT FALSE;
ALTER TABLE comments ADD COLUMN moderated_by INTEGER;
ALTER TABLE comments ADD COLUMN moderated_at TIMESTAMP;
ALTER TABLE comments ADD COLUMN spam_score DECIMAL(3,2);
```

**Next.js Pages:**
```
/admin/comments                      # All comments dashboard
/admin/comments/pending              # Comment moderation queue
/admin/comments/reported             # Reported comments
/admin/comments/spam                 # Spam detection results
/admin/comments/[id]                 # Individual comment review
```

**Components:**
```
/src/components/admin/comments/
├── CommentModerationTable.tsx       # Comment list with actions
├── CommentReviewCard.tsx            # Comment with context
├── CommentBulkActions.tsx           # Batch moderation tools
├── SpamIndicator.tsx                # Spam score visualization
├── CommentThread.tsx                # Thread context view
└── CommentUserProfile.tsx           # Commenter info sidebar
```

**Dependencies**: Phase 1 (Admin foundation)

---

## Task B4: Basic Analytics Dashboard
- **Priority**: P1 (High)
- **Estimated Time**: 8 hours  
- **Status**: TODO
- **Based on**: Task 58 from original admin features (basic version)

**Frontend Requirements:**
- Overview metrics dashboard
- User engagement charts
- Content performance graphs
- Real-time statistics
- Exportable reports

**Backend Requirements:**
- Analytics data aggregation
- Real-time metrics API
- Performance calculations
- Data export functionality

**API Endpoints:**
```
GET /api/admin/analytics/overview    # Dashboard summary metrics
GET /api/admin/analytics/users       # User engagement data
GET /api/admin/analytics/content     # Content performance metrics
GET /api/admin/analytics/comments    # Comment engagement stats
GET /api/admin/analytics/traffic     # Traffic and activity data
GET /api/admin/analytics/export      # Export analytics data
```

**Next.js Pages:**
```
/admin/dashboard                     # Main analytics dashboard
/admin/analytics                     # Detailed analytics page
/admin/analytics/users               # User analytics
/admin/analytics/content             # Content analytics
/admin/analytics/reports             # Report generation
```

**Components:**
```
/src/components/admin/analytics/
├── OverviewCards.tsx                # Key metric cards
├── UserEngagementChart.tsx          # User activity graphs
├── ContentPerformanceChart.tsx      # Post/comment metrics
├── TrafficChart.tsx                 # Traffic visualization
├── ExportButton.tsx                 # Data export controls
└── DateRangePicker.tsx              # Time period selector
```

**Key Metrics to Track:**
- Total users, posts, comments
- Daily/weekly/monthly active users  
- Most popular posts
- Comment engagement rates
- User registration trends
- Content publication patterns

**Dependencies**: Phase 1 (Admin foundation)

---

## Phase 2 Definition of Done

- [ ] Admin can view and manage all users
- [ ] User roles can be assigned and modified
- [ ] Content moderation workflow is functional
- [ ] Posts can be approved, rejected, or scheduled
- [ ] Comments can be moderated and spam-filtered
- [ ] Basic analytics dashboard shows key metrics
- [ ] All admin actions are logged for audit
- [ ] Bulk operations work for users and content
- [ ] Export functionality works for reports
- [ ] Mobile restrictions remain enforced

---

## Database Schema Updates for Phase 2

```sql
-- User management enhancements
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
ALTER TABLE users ADD COLUMN suspension_reason TEXT;

-- Post moderation system
ALTER TABLE blog_posts ADD COLUMN status VARCHAR(20) DEFAULT 'draft';
ALTER TABLE blog_posts ADD COLUMN featured BOOLEAN DEFAULT FALSE;
ALTER TABLE blog_posts ADD COLUMN moderated_by INTEGER;
ALTER TABLE blog_posts ADD COLUMN moderated_at TIMESTAMP;
ALTER TABLE blog_posts ADD COLUMN rejection_reason TEXT;
ALTER TABLE blog_posts ADD COLUMN scheduled_publish TIMESTAMP;

-- Comment moderation system  
ALTER TABLE comments ADD COLUMN status VARCHAR(20) DEFAULT 'approved';
ALTER TABLE comments ADD COLUMN is_spam BOOLEAN DEFAULT FALSE;
ALTER TABLE comments ADD COLUMN moderated_by INTEGER;
ALTER TABLE comments ADD COLUMN moderated_at TIMESTAMP;
ALTER TABLE comments ADD COLUMN spam_score DECIMAL(3,2);

-- Audit logging table
CREATE TABLE admin_audit_logs (
    id SERIAL PRIMARY KEY,
    admin_user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id INTEGER,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Analytics aggregation tables
CREATE TABLE daily_stats (
    date DATE PRIMARY KEY,
    new_users INTEGER DEFAULT 0,
    new_posts INTEGER DEFAULT 0,
    new_comments INTEGER DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Testing Requirements for Phase 2

### Backend Tests
- [ ] User management API endpoints work correctly
- [ ] Content moderation workflow functions properly
- [ ] Comment moderation and spam detection work
- [ ] Analytics data is calculated accurately
- [ ] Audit logging captures all admin actions
- [ ] Bulk operations handle edge cases

### Frontend Tests
- [ ] User management interface works end-to-end
- [ ] Content moderation queue updates properly
- [ ] Comment moderation tools function correctly
- [ ] Analytics dashboard displays accurate data
- [ ] Export functionality works for all data types
- [ ] Mobile restrictions still enforced

### Performance Tests
- [ ] User list pagination works with large datasets
- [ ] Analytics queries complete within 3 seconds
- [ ] Bulk operations handle large selections
- [ ] Real-time dashboard updates efficiently

---

## Security Considerations for Phase 2

### Access Control
- [ ] All admin endpoints verify admin role
- [ ] Sensitive user data is properly protected
- [ ] Audit logs cannot be modified by admins
- [ ] Export functions include access controls

### Data Protection
- [ ] User PII is handled according to privacy policies
- [ ] Admin actions are logged with full context
- [ ] Deleted content is properly anonymized
- [ ] Analytics data excludes sensitive information

### Input Validation
- [ ] All admin forms validate input server-side
- [ ] Bulk operations validate all items
- [ ] File uploads (if any) are properly sanitized
- [ ] SQL injection protection on all queries