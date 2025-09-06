# Admin Dashboard Implementation Tasks

## Phase 1: Foundation & Authentication (Week 1-2)

### Task A1: User Role System (Backend)
- **Priority**: P0 (Critical)
- **Estimated Time**: 6 hours
- **Status**: TODO

**Requirements:**
- Add `role` enum field to User model (`user`, `admin`, `super_admin`)
- Create database migration for role field
- Update user registration to default to `user` role
- Modify admin test user to have `admin` role

**API Changes Needed:**
```python
# In models/models.py
from sqlalchemy import Enum
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin" 
    SUPER_ADMIN = "super_admin"

# Add to User model:
role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
```

**Database Migration:**
```sql
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user' NOT NULL;
UPDATE users SET role = 'admin' WHERE username = 'admin';
```

**Dependencies**: None
**Deliverables**: 
- Updated User model with role field
- Database migration script
- Unit tests for role functionality

---

### Task A2: Admin Middleware & Route Protection (Backend)
- **Priority**: P0 (Critical)
- **Estimated Time**: 4 hours
- **Status**: TODO

**Requirements:**
- Create admin role verification middleware
- Add admin-only route decorators
- Implement role-based endpoint protection
- Create admin user dependency for FastAPI

**Implementation:**
```python
# In auth/auth.py
async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Usage in routers
@router.get("/admin/users")
async def get_all_users(admin_user: User = Depends(get_current_admin_user)):
    # Admin endpoint logic
```

**Dependencies**: Task A1 (User Role System)
**Deliverables**:
- Admin middleware functions
- Route protection decorators
- Integration tests for admin access

---

### Task A3: Admin Layout & Navigation (Frontend)
- **Priority**: P1 (High)
- **Estimated Time**: 8 hours
- **Status**: TODO

**Requirements:**
- Create admin layout component with sidebar navigation
- Build admin header with user info and logout
- Implement breadcrumb navigation
- Design responsive admin interface (desktop-only)

**Components to Create:**
```
/src/components/admin/
├── AdminLayout.tsx          # Main admin layout wrapper
├── AdminSidebar.tsx         # Navigation sidebar
├── AdminHeader.tsx          # Admin header with user menu
├── AdminBreadcrumb.tsx      # Breadcrumb navigation
└── AdminLoadingSkeleton.tsx # Loading states
```

**Navigation Structure:**
- Dashboard
- Users Management
- Content Moderation  
- Comments
- Analytics
- Settings
- Tools

**Dependencies**: None (can work in parallel)
**Deliverables**:
- Admin layout components
- Navigation system
- Mobile restriction implementation

---

### Task A4: Desktop-Only Access Restrictions
- **Priority**: P1 (High)
- **Estimated Time**: 4 hours
- **Status**: TODO

**Requirements:**
- Implement browser detection for mobile devices
- Create middleware to redirect mobile users
- Build mobile restriction page with explanation
- Add responsive design breakpoints for admin

**Implementation Strategy:**
1. **Next.js Middleware** for server-side detection
2. **CSS Media Queries** for responsive restrictions
3. **JavaScript Detection** for dynamic checking
4. **User-Agent Parsing** for mobile device identification

**Files to Create:**
```
/src/middleware.ts                    # Route protection middleware
/src/app/admin/mobile-not-supported/  # Mobile restriction page
/src/styles/admin.css                 # Admin-specific styles
```

**Dependencies**: None
**Deliverables**:
- Mobile detection and redirection
- Responsive admin interface
- Mobile restriction page

---

## Phase 1 Definition of Done

- [ ] User model has role field with enum values
- [ ] Admin middleware protects admin routes
- [ ] Admin layout renders with proper navigation
- [ ] Mobile users are blocked from admin area
- [ ] All admin components are desktop-optimized
- [ ] Role-based authentication works end-to-end
- [ ] Admin user can log in and see admin dashboard
- [ ] Regular users cannot access admin routes

---

## API Endpoints for Phase 1

### Authentication Extensions
```
GET  /api/auth/me                    # Include user role in response
POST /api/auth/admin/verify          # Verify admin session
```

### Admin User Management (Basic)
```
GET /api/admin/users                 # List all users (admin only)
GET /api/admin/users/{id}            # Get user details (admin only)
```

---

## Next.js Pages for Phase 1

### Admin Routes
```
/admin                               # Admin dashboard (placeholder)
/admin/login                         # Admin login (if separate from main)
/admin/mobile-not-supported          # Mobile restriction page
```

### Layout Structure
```
AdminLayout
├── AdminHeader (user menu, logout)
├── AdminSidebar (navigation menu)
└── AdminContent (page content area)
```

---

## Testing Requirements for Phase 1

### Backend Tests
- [ ] User role assignment and validation
- [ ] Admin middleware blocks non-admin users
- [ ] Admin endpoints require admin role
- [ ] Role-based authentication flow

### Frontend Tests
- [ ] Admin layout renders correctly
- [ ] Navigation works for all admin routes
- [ ] Mobile detection redirects properly
- [ ] Admin pages are desktop-only

### Integration Tests
- [ ] Admin user can access admin area
- [ ] Regular user cannot access admin area
- [ ] Mobile browser is redirected
- [ ] Admin authentication flow works

---

## Risk Mitigation

### Technical Risks
1. **Database Migration**: Test migration on copy of production data
2. **Authentication Breaking**: Implement gradual rollout with feature flags
3. **Mobile Detection**: Test across multiple browsers and devices
4. **Performance**: Monitor admin page load times

### Security Risks
1. **Role Escalation**: Implement proper role validation on all endpoints
2. **Session Hijacking**: Use secure JWT tokens with short expiration
3. **Admin Access**: Implement audit logging for all admin actions
4. **CSRF Protection**: Add CSRF tokens to admin forms

### Deployment Risks
1. **Backward Compatibility**: Ensure existing user authentication still works
2. **Database Migration**: Plan for zero-downtime migration
3. **Feature Rollback**: Prepare rollback plan for admin features
4. **Monitoring**: Set up alerts for admin authentication failures