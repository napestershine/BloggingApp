# SF5 Blog App

A Flutter mobile application that integrates with the SF5 Blog API built with Symfony.

## Features

- **User Authentication**: Login and registration with JWT tokens
- **Blog Management**: Create, read, and browse blog posts
- **Comments**: Add and view comments on blog posts
- **Responsive UI**: Modern Material Design interface
- **State Management**: Uses Provider for efficient state management
- **HTTP Integration**: Connects to Symfony API Platform endpoints

## Getting Started

### Prerequisites

- Flutter SDK (3.0.0 or higher)
- Dart SDK
- Android Studio / VS Code with Flutter extensions
- Running SF5 Blog API server

### Installation

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   flutter pub get
   ```

3. Generate model files (if needed):
   ```bash
   flutter packages pub run build_runner build
   ```

### Configuration

1. **API Base URL**: Update the base URL in `lib/utils/api_config.dart` to match your Symfony API server:
   ```dart
   static const String defaultBaseUrl = 'http://your-api-server.com/api';
   ```

2. **Development URLs**:
   - **Android Emulator**: Use `http://10.0.2.2:8080/api`
   - **iOS Simulator**: Use `http://localhost:8080/api`
   - **Physical Device**: Use your computer's IP address, e.g., `http://192.168.1.100:8080/api`

### Running the App

1. Start your Symfony API server:
   ```bash
   # In the parent directory
   docker compose up -d
   # or
   php bin/console server:run
   ```

2. Run the Flutter app:
   ```bash
   flutter run
   ```

## Project Structure

```
app/
├── lib/
│   ├── main.dart                 # App entry point
│   ├── models/                   # Data models
│   │   ├── user.dart
│   │   ├── blog_post.dart
│   │   └── comment.dart
│   ├── services/                 # Business logic
│   │   ├── auth_service.dart     # Authentication
│   │   └── api_service.dart      # API communication
│   ├── screens/                  # UI screens
│   │   ├── login_screen.dart
│   │   ├── blog_list_screen.dart
│   │   ├── blog_detail_screen.dart
│   │   └── create_post_screen.dart
│   ├── widgets/                  # Reusable widgets
│   │   ├── blog_post_card.dart
│   │   └── comment_card.dart
│   └── utils/                    # Utilities
│       └── api_config.dart
├── android/                      # Android-specific files
├── ios/                          # iOS-specific files
├── test/                         # Unit tests
├── pubspec.yaml                  # Dependencies
└── analysis_options.yaml        # Linting rules
```

## API Integration

The app integrates with the following SF5 API endpoints:

- `POST /api/login_check` - User authentication
- `POST /api/users` - User registration
- `GET /api/blog_posts` - Fetch blog posts
- `POST /api/blog_posts` - Create new blog post
- `GET /api/blog_posts/{id}` - Fetch specific blog post
- `GET /api/blog_posts/{id}/comments` - Fetch comments for a blog post
- `POST /api/comments` - Create new comment

## Key Features

### Authentication
- JWT token-based authentication
- Secure token storage using SharedPreferences
- Automatic token inclusion in API requests
- Login/logout functionality

### Blog Posts
- List all blog posts with pagination support
- View detailed blog post with author information
- Create new blog posts with validation
- Auto-generate URL slugs from titles

### Comments
- View comments on blog posts
- Add new comments to posts
- Real-time comment updates

### UI/UX
- Material Design 3 theming
- Responsive layouts for different screen sizes
- Loading states and error handling
- Form validation with user feedback
- Pull-to-refresh functionality

## Dependencies

- **flutter**: Flutter framework
- **http**: HTTP client for API calls
- **provider**: State management
- **go_router**: Declarative routing
- **shared_preferences**: Local data storage
- **json_annotation**: JSON serialization support

## Development

### Adding New Features

1. **Models**: Add new data models in `lib/models/`
2. **Services**: Extend API services in `lib/services/`
3. **Screens**: Create new screens in `lib/screens/`
4. **Widgets**: Add reusable components in `lib/widgets/`

### Testing

Run unit tests:
```bash
flutter test
```

### Building

Build for Android:
```bash
flutter build apk
```

Build for iOS:
```bash
flutter build ios
```

## Troubleshooting

### Common Issues

1. **API Connection Issues**:
   - Ensure the Symfony server is running
   - Check the API base URL configuration
   - Verify network permissions in AndroidManifest.xml

2. **Authentication Problems**:
   - Clear app data/cache
   - Check JWT token validity
   - Verify API credentials

3. **Build Issues**:
   - Run `flutter clean` and `flutter pub get`
   - Check Flutter version compatibility
   - Verify all dependencies are properly installed

### Network Configuration

For development, ensure your API server is accessible:

- **Local Development**: Use `http://localhost:8080/api`
- **Docker**: Use `http://localhost:8080/api` or the container IP
- **Physical Device**: Use your computer's IP address

## Contributing

1. Follow Flutter/Dart coding standards
2. Add tests for new features
3. Update documentation as needed
4. Use meaningful commit messages