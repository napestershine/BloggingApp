# BloggingApp Sample Credentials

This document provides sample credentials and testing instructions for the BloggingApp user experience features.

## 🌱 Database Seeding (Recommended)

The fastest way to get started is using the built-in database seeding system:

```bash
cd python
python seed.py up
```

This creates a complete dataset with users, blog posts, and comments for immediate testing.

## 🔐 Seeded User Accounts

After running `python seed.py up`, you'll have these accounts available:

### 👤 Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@blogapp.com`
- **Name**: Admin User
- **Role**: Admin
- **Status**: Email verified ✅
- **Bio**: Site administrator with full privileges.
- **Features**: Full system access, content moderation

### ✍️ Editor Account
- **Username**: `editor`
- **Password**: `editor123`
- **Email**: `editor@blogapp.com`
- **Name**: Editor Smith
- **Role**: User (with editor capabilities)
- **Status**: Email verified ✅
- **Bio**: Content editor and writer.
- **Features**: Content creation and editing

### 👥 Regular User Accounts

#### User 1 - John Doe
- **Username**: `user1`
- **Password**: `user123`
- **Email**: `user1@blogapp.com`
- **Name**: John Doe
- **Role**: User
- **Status**: Email verified ✅
- **Bio**: Regular user who loves reading and commenting on blogs.

#### User 2 - Jane Smith
- **Username**: `user2`
- **Password**: `user123`
- **Email**: `user2@blogapp.com`
- **Name**: Jane Smith
- **Role**: User
- **Status**: Email verified ✅
- **Bio**: Technology enthusiast and blogger.

## 📝 Sample Content

The seeding system also creates sample blog posts and comments:

### Blog Posts
1. **"Welcome to Our Blog Platform"** - Featured welcome post
2. **"Getting Started with Blogging"** - Tips for beginners
3. **"The Future of Web Development"** - Technology insights
4. **"Draft Post - Work in Progress"** - Example draft content

### Comments
- Interactive comments on published posts
- Threaded discussions between users
- Approved comments ready for testing

## 🚀 Quick Start Testing

### 1. Seed the Database
```bash
cd python
python seed.py up
```

### 2. Start the Backend API
```bash
uvicorn app.main:app --reload
```

### 3. Test Authentication
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

### 4. Explore Sample Data
- **API Documentation**: http://localhost:8000/docs
- **View Posts**: `GET /blog_posts/`
- **View Comments**: `GET /comments/`
- **User Profiles**: `GET /users/{user_id}/`

## 📱 Flutter App Testing

### 1. Start the Flutter App
```bash
cd app
flutter pub get
flutter run
```

### 2. Login with Sample Credentials
Use any of the sample credentials above to test the Flutter authentication flow.

### 3. Test Complete User Journey
1. **Login** with sample credentials
2. **View Profile** - Check user information
3. **Update Profile** - Modify bio and social links
4. **Refresh Token** - Test token management
5. **Logout** - Clear authentication state

## 🧪 Comprehensive Test Coverage

### Backend API Tests
Run the complete test suite:
```bash
cd python
python -m pytest app/tests/test_user_features.py -v
```

### Test Cases Covered
- ✅ User registration and login
- ✅ Email verification flow
- ✅ Password reset functionality  
- ✅ User profile management
- ✅ Token refresh and logout
- ✅ Sample credentials validation
- ✅ Complete user journey testing
- ✅ Error handling and edge cases

### Flutter Tests
```bash
cd app
flutter test test/services/auth_service_test.dart
```

## 🔗 Available API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/refresh` - Refresh access token

### Email Verification
- `POST /auth/verify-email` - Request email verification
- `POST /auth/verify-email/confirm` - Confirm email verification

### Password Reset
- `POST /auth/password/forgot` - Request password reset
- `POST /auth/password/reset` - Reset password with token

### User Management
- `GET /users/{id}/profile` - Get user profile
- `PUT /users/{id}/profile` - Update user profile
- `POST /users/upload/avatar` - Upload user avatar

### Documentation
- `GET /docs` - Interactive Swagger documentation
- `GET /redoc` - ReDoc documentation

## 🛠 Development Features Implemented

### ✅ Completed User Experience Tasks

1. **Enhanced User Registration** - Complete registration with email verification
2. **User Profile Management** - Full profile CRUD with avatar upload
3. **Password Reset Functionality** - Forgot/reset password flow
4. **Authentication State Management** - Token refresh and logout
5. **Sample Credentials** - Pre-populated test accounts
6. **Comprehensive Testing** - Full test coverage for all features

### 🚧 Flutter Integration Status
- ✅ AuthService with all endpoint methods
- ✅ State management with Provider
- ✅ Token persistence with SharedPreferences
- ✅ Comprehensive Flutter tests
- ✅ Error handling and loading states

## 📊 Testing Statistics

- **Backend Tests**: 9/9 passing ✅
- **Flutter Tests**: Comprehensive coverage ✅
- **API Endpoints**: 12 endpoints implemented ✅
- **Sample Users**: 4 test accounts ready ✅
- **Authentication Flow**: Complete journey tested ✅

## 🎯 Next Steps

1. **Run the backend API**: `uvicorn app.main:app --reload`
2. **Start the Flutter app**: `flutter run`
3. **Login with sample credentials** above
4. **Explore all features** through the UI and API
5. **Run tests** to verify functionality

---

**Need Help?** Check the interactive API documentation at `http://localhost:8000/docs` when the backend is running.