class ApiConfig {
  // API Configuration
  static const String defaultBaseUrl = 'http://localhost:8080/api';
  
  // You can override this in a local config file or environment variables
  static String get baseUrl {
    // For production, you would want to use your actual domain
    // For development with Android emulator, use 10.0.2.2:8080
    // For development with iOS simulator, use localhost:8080
    // For development with physical device, use your computer's IP address
    
    return const String.fromEnvironment(
      'API_BASE_URL',
      defaultValue: defaultBaseUrl,
    );
  }
  
  // API Endpoints
  static const String loginEndpoint = '/login_check';
  static const String usersEndpoint = '/users';
  static const String blogPostsEndpoint = '/blog_posts';
  static const String commentsEndpoint = '/comments';
  
  // Request timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  // Storage keys
  static const String tokenStorageKey = 'jwt_token';
  static const String userStorageKey = 'user_data';
}