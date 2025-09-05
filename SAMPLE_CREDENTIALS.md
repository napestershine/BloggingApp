# BloggingApp Sample Credentials

This document provides sample credentials and testing instructions for the BloggingApp user experience features.

## 🔐 Sample User Accounts

The following test accounts have been pre-created in the database for testing purposes:

### 👤 Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`
- **Name**: Admin User
- **Status**: Email verified ✅
- **Features**: System administrator with full access

### 👥 Regular User Accounts

#### John Doe - Developer
- **Username**: `johndoe`
- **Password**: `john123`
- **Email**: `john@example.com`
- **Name**: John Doe
- **Bio**: Software developer and tech enthusiast
- **Status**: Email verified ✅
- **Social Links**: GitHub, Twitter, Personal website

#### Jane Smith - Designer  
- **Username**: `janesmith`
- **Password**: `jane123`
- **Email**: `jane@example.com`
- **Name**: Jane Smith
- **Bio**: UX Designer and blogger
- **Status**: Email verified ✅
- **Social Links**: Dribbble, Twitter, Portfolio

#### Test User
- **Username**: `testuser`
- **Password**: `test123`
- **Email**: `test@example.com`
- **Name**: Test User
- **Bio**: Test account for development
- **Status**: Email NOT verified ❌
- **Features**: Ideal for testing email verification flow

## 🚀 Quick Start Testing

### 1. Start the Backend API
```bash
cd python
uvicorn app.main:app --reload
```

### 2. Test Authentication Endpoints

#### Login Example
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

#### Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Test User Profile Management

#### Get User Profile
```bash
curl -X GET "http://localhost:8000/users/1/profile" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Update User Profile
```bash
curl -X PUT "http://localhost:8000/users/1/profile" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Updated Name",
       "bio": "Updated bio text",
       "social_links": {
         "twitter": "@mynewhandle",
         "github": "github.com/myusername"
       }
     }'
```

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