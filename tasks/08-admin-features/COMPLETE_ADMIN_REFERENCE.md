# Complete Admin Dashboard: Endpoints & Pages Reference

## Summary

This document provides a complete reference of all API endpoints and Next.js pages required for the BloggingApp admin dashboard implementation.

## Recommended Approach: Integrated Admin Dashboard

**✅ RECOMMENDED**: Implement admin dashboard within existing Next.js application at `/admin/*` routes.

**Key Benefits:**
- Shared authentication and API infrastructure
- Faster development using existing components
- Single deployment and maintenance
- Desktop-only access through responsive design and route guards
- Future migration path to separate app if needed

---

## Complete API Endpoints Reference

### Authentication & Authorization
```
GET  /api/auth/me                      # Include user role in response
POST /api/auth/admin/login             # Admin-specific login (optional)
GET  /api/auth/admin/verify            # Verify admin session
PUT  /api/auth/admin/permissions       # Update user permissions
```

### User Management
```
GET    /api/admin/users                # List all users (paginated)
GET    /api/admin/users/{id}           # Get user details
PUT    /api/admin/users/{id}           # Update user (role, status)
DELETE /api/admin/users/{id}           # Delete/suspend user
POST   /api/admin/users/{id}/roles     # Assign roles
GET    /api/admin/users/stats          # User statistics
POST   /api/admin/users/bulk           # Bulk user operations
GET    /api/admin/users/activity       # User activity logs
```

### Content Management
```
GET    /api/admin/posts                # All posts with moderation status
GET    /api/admin/posts/pending        # Posts awaiting moderation
GET    /api/admin/posts/reported       # Reported posts
PUT    /api/admin/posts/{id}/status    # Approve/reject/schedule posts
DELETE /api/admin/posts/{id}           # Delete posts
POST   /api/admin/posts/bulk           # Bulk post operations
GET    /api/admin/posts/stats          # Content statistics
POST   /api/admin/posts/{id}/feature   # Feature/unfeature posts
```

### Comment Moderation
```
GET    /api/admin/comments             # All comments with filters
GET    /api/admin/comments/pending     # Comments awaiting moderation
GET    /api/admin/comments/reported    # Reported comments
PUT    /api/admin/comments/{id}/status # Approve/reject comments
DELETE /api/admin/comments/{id}        # Delete comments
POST   /api/admin/comments/bulk        # Bulk comment operations
GET    /api/admin/comments/spam        # Spam detection queue
GET    /api/admin/comments/user/{id}   # User's comment history
```

### Analytics & Reporting
```
GET  /api/admin/analytics/overview     # Dashboard summary metrics
GET  /api/admin/analytics/users        # User engagement data
GET  /api/admin/analytics/content      # Content performance metrics
GET  /api/admin/analytics/comments     # Comment engagement stats
GET  /api/admin/analytics/traffic      # Traffic and activity data
GET  /api/admin/analytics/dashboard    # Configurable dashboard data
GET  /api/admin/analytics/timeseries   # Time-series metrics
GET  /api/admin/analytics/compare      # Period comparison data
GET  /api/admin/analytics/segments     # User/content segmentation
GET  /api/admin/analytics/funnel       # User journey analytics
GET  /api/admin/analytics/retention    # User retention metrics
POST /api/admin/analytics/custom       # Custom query builder
GET  /api/admin/analytics/export       # Export analytics data
```

### Reports Management
```
GET  /api/admin/reports                # Scheduled reports list
POST /api/admin/reports                # Create scheduled report
GET  /api/admin/reports/{id}           # Get report details
GET  /api/admin/reports/{id}/download  # Download report file
PUT  /api/admin/reports/{id}           # Update report settings
DELETE /api/admin/reports/{id}         # Delete scheduled report
```

### System Settings
```
GET  /api/admin/settings               # Get all settings by category
GET  /api/admin/settings/{category}    # Get specific category settings
PUT  /api/admin/settings/{category}    # Update category settings
POST /api/admin/settings/validate      # Validate settings before save
GET  /api/admin/settings/export        # Export settings configuration
POST /api/admin/settings/import        # Import settings configuration
GET  /api/admin/settings/history       # Settings change history
POST /api/admin/settings/rollback      # Rollback to previous version
```

### Backup & Maintenance
```
GET    /api/admin/backup               # List all backups
POST   /api/admin/backup               # Create new backup
GET    /api/admin/backup/{id}          # Get backup details
POST   /api/admin/backup/{id}/restore  # Restore from backup
DELETE /api/admin/backup/{id}          # Delete backup
GET    /api/admin/backup/schedule      # Get backup schedule
PUT    /api/admin/backup/schedule      # Update backup schedule

GET  /api/admin/health                 # System health status
GET  /api/admin/health/database        # Database health metrics
GET  /api/admin/health/api             # API performance metrics
GET  /api/admin/health/storage         # Storage usage metrics

GET  /api/admin/logs                   # Application logs
GET  /api/admin/logs/{type}            # Specific log type
GET  /api/admin/logs/errors            # Error log analysis
GET  /api/admin/logs/performance       # Performance logs

POST /api/admin/maintenance/optimize   # Optimize database
POST /api/admin/maintenance/cleanup    # Clean temporary files
GET  /api/admin/maintenance/status     # Maintenance status
POST /api/admin/maintenance/schedule   # Schedule maintenance
```

### Audit & Security
```
GET  /api/admin/audit                  # Get audit logs with filters
GET  /api/admin/audit/{id}             # Get specific audit entry
GET  /api/admin/audit/user/{id}        # Get user's audit history
GET  /api/admin/audit/export           # Export audit data
GET  /api/admin/audit/security         # Security-related events
GET  /api/admin/audit/anomalies        # Detected anomalies
POST /api/admin/audit/flag             # Flag suspicious activity
```

---

## Complete Next.js Pages Reference

### Layout & Authentication
```
/admin                                 # Admin dashboard layout
/admin/login                           # Admin login page (if separate)
/admin/mobile-not-supported            # Mobile restriction page
```

### Dashboard & Overview
```
/admin/dashboard                       # Main admin dashboard
/admin/analytics                       # Analytics overview page
```

### User Management
```
/admin/users                           # User list with search/filter
/admin/users/[id]                      # Individual user details
/admin/users/[id]/edit                 # Edit user form
/admin/users/new                       # Create new admin user
/admin/users/activity                  # User activity dashboard
```

### Content Management
```
/admin/posts                           # All posts with moderation status
/admin/posts/pending                   # Posts awaiting approval
/admin/posts/reported                  # Reported posts queue
/admin/posts/scheduled                 # Scheduled posts
/admin/posts/[id]                      # Individual post review
/admin/posts/[id]/edit                 # Admin post editing
```

### Comment Moderation
```
/admin/comments                        # All comments with filters
/admin/comments/pending                # Comment moderation queue
/admin/comments/reported               # Reported comments
/admin/comments/spam                   # Spam detection results
/admin/comments/[id]                   # Individual comment review
```

### Analytics & Reporting
```
/admin/analytics/dashboard             # Interactive analytics dashboard
/admin/analytics/users                 # Deep user analytics
/admin/analytics/content               # Content performance analytics
/admin/analytics/community             # Community engagement metrics
/admin/analytics/performance           # System performance metrics
/admin/analytics/custom                # Custom query builder
/admin/reports                         # Report management
/admin/reports/[id]                    # Individual report view
```

### System Management
```
/admin/settings                        # Settings dashboard
/admin/settings/general                # General site settings
/admin/settings/content                # Content management settings
/admin/settings/users                  # User management settings
/admin/settings/notifications          # Notification configuration
/admin/settings/security               # Security settings
/admin/settings/performance            # Performance configuration
/admin/settings/import-export          # Settings backup/restore
```

### Tools & Maintenance
```
/admin/tools                           # Admin tools dashboard
/admin/tools/backup                    # Backup management
/admin/tools/health                    # System health monitor
/admin/tools/logs                      # Log viewer and analysis
/admin/tools/maintenance               # Maintenance tasks
/admin/tools/performance               # Performance monitoring
```

### Audit & Security
```
/admin/audit                           # Audit log viewer
/admin/audit/security                  # Security events
/admin/audit/user/[id]                 # User-specific audit trail
```

---

## Database Schema Requirements

### User Model Extensions
```sql
-- Add role and status fields to users table
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user' NOT NULL;
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
ALTER TABLE users ADD COLUMN suspension_reason TEXT;

-- Update admin user role
UPDATE users SET role = 'admin' WHERE username = 'admin';
```

### Content Moderation Schema
```sql
-- Add moderation fields to blog_posts table
ALTER TABLE blog_posts ADD COLUMN status VARCHAR(20) DEFAULT 'draft';
ALTER TABLE blog_posts ADD COLUMN featured BOOLEAN DEFAULT FALSE;
ALTER TABLE blog_posts ADD COLUMN moderated_by INTEGER;
ALTER TABLE blog_posts ADD COLUMN moderated_at TIMESTAMP;
ALTER TABLE blog_posts ADD COLUMN rejection_reason TEXT;
ALTER TABLE blog_posts ADD COLUMN scheduled_publish TIMESTAMP;

-- Add moderation fields to comments table
ALTER TABLE comments ADD COLUMN status VARCHAR(20) DEFAULT 'approved';
ALTER TABLE comments ADD COLUMN is_spam BOOLEAN DEFAULT FALSE;
ALTER TABLE comments ADD COLUMN moderated_by INTEGER;
ALTER TABLE comments ADD COLUMN moderated_at TIMESTAMP;
ALTER TABLE comments ADD COLUMN spam_score DECIMAL(3,2);
```

### Admin-Specific Tables
```sql
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

-- System settings table
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL,
    data_type VARCHAR(20) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(category, key)
);

-- Settings history table
CREATE TABLE settings_history (
    id SERIAL PRIMARY KEY,
    setting_id INTEGER REFERENCES system_settings(id),
    old_value JSONB,
    new_value JSONB,
    changed_by INTEGER REFERENCES users(id),
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Backup management table
CREATE TABLE system_backups (
    id SERIAL PRIMARY KEY,
    backup_type VARCHAR(20) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    compression_ratio DECIMAL(4,2),
    status VARCHAR(20) DEFAULT 'completed',
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    notes TEXT
);

-- Health metrics table
CREATE TABLE system_health_metrics (
    id SERIAL PRIMARY KEY,
    metric_type VARCHAR(50) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DECIMAL(10,4) NOT NULL,
    unit VARCHAR(20),
    status VARCHAR(20) DEFAULT 'normal',
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Daily statistics table
CREATE TABLE daily_stats (
    date DATE PRIMARY KEY,
    new_users INTEGER DEFAULT 0,
    new_posts INTEGER DEFAULT 0,
    new_comments INTEGER DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Maintenance tasks table
CREATE TABLE maintenance_tasks (
    id SERIAL PRIMARY KEY,
    task_name VARCHAR(100) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    schedule_expression VARCHAR(100),
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    status VARCHAR(20) DEFAULT 'enabled',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Component Architecture

### Admin Layout Structure
```
AdminLayout
├── AdminHeader
│   ├── AdminUserMenu
│   ├── NotificationBell
│   └── AdminSearch
├── AdminSidebar
│   ├── AdminNavigation
│   ├── QuickActions
│   └── AdminFooter
└── AdminContent
    ├── AdminBreadcrumb
    ├── PageHeader
    └── PageContent
```

### Key Component Categories
```
/src/components/admin/
├── layout/                    # Layout components
│   ├── AdminLayout.tsx
│   ├── AdminSidebar.tsx
│   ├── AdminHeader.tsx
│   └── AdminBreadcrumb.tsx
├── users/                     # User management
│   ├── UserTable.tsx
│   ├── UserEditForm.tsx
│   └── UserStats.tsx
├── posts/                     # Content management
│   ├── PostModerationQueue.tsx
│   ├── PostReviewCard.tsx
│   └── PostBulkActions.tsx
├── comments/                  # Comment moderation
│   ├── CommentModerationTable.tsx
│   ├── CommentReviewCard.tsx
│   └── SpamIndicator.tsx
├── analytics/                 # Analytics & reporting
│   ├── OverviewCards.tsx
│   ├── InteractiveChart.tsx
│   └── CustomQueryBuilder.tsx
├── settings/                  # System settings
│   ├── SettingsForm.tsx
│   ├── SettingsPreview.tsx
│   └── ImportExportPanel.tsx
├── tools/                     # Admin tools
│   ├── BackupManager.tsx
│   ├── HealthDashboard.tsx
│   └── LogViewer.tsx
└── common/                    # Shared components
    ├── AdminTable.tsx
    ├── AdminModal.tsx
    ├── AdminButton.tsx
    └── AdminLoadingSkeleton.tsx
```

---

## Desktop-Only Implementation

### 1. Next.js Middleware
```typescript
// src/middleware.ts
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/admin')) {
    const userAgent = request.headers.get('user-agent') || '';
    const isMobile = /Mobile|Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i.test(userAgent);
    
    if (isMobile) {
      return NextResponse.redirect(new URL('/admin/mobile-not-supported', request.url));
    }
  }
}
```

### 2. CSS Media Queries
```css
/* Admin styles - desktop only */
@media (max-width: 1024px) {
  .admin-layout {
    display: none;
  }
  .mobile-restriction-message {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    text-align: center;
  }
}
```

### 3. React Component Detection
```typescript
// Admin layout component
useEffect(() => {
  if (typeof window !== 'undefined' && window.innerWidth < 1024) {
    router.push('/admin/mobile-not-supported');
  }
}, [router]);
```

---

## Implementation Timeline

### Phase 1: Foundation (Week 1-2)
- ✅ User role system
- ✅ Admin route protection
- ✅ Admin layout components
- ✅ Desktop-only restrictions

### Phase 2: Core Features (Week 3-4)
- ✅ User management interface
- ✅ Content moderation dashboard
- ✅ Comment moderation tools
- ✅ Basic analytics dashboard

### Phase 3: Advanced Features (Week 5-6)
- ✅ Advanced analytics & reporting
- ✅ System settings management
- ✅ Backup & maintenance tools
- ✅ Admin audit system

### Total Estimated Time: 6 weeks (62 hours)

---

## Success Criteria

1. **Functionality**: All admin tasks implemented and working
2. **Security**: Role-based access control enforced
3. **Usability**: Intuitive admin interface for desktop users
4. **Performance**: Admin dashboard loads within 2 seconds
5. **Mobile Restriction**: Mobile users properly blocked/redirected
6. **Audit Trail**: All admin actions logged and traceable
7. **Scalability**: System handles growing user base efficiently
8. **Maintainability**: Clean, documented codebase for future updates

This comprehensive admin dashboard will provide the BloggingApp with professional-grade administrative capabilities while maintaining the desktop-only requirement and leveraging the existing Next.js infrastructure.