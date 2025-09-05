import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sf5_blog_app/services/auth_service.dart';
import 'package:sf5_blog_app/models/user.dart';

import 'auth_service_test.mocks.dart';

@GenerateMocks([http.Client])
void main() {
  group('AuthService Tests', () {
    late AuthService authService;
    late MockClient mockHttpClient;

    setUp(() {
      mockHttpClient = MockClient();
      authService = AuthService();
      
      // Initialize SharedPreferences for testing
      SharedPreferences.setMockInitialValues({});
    });

    tearDown(() {
      authService.dispose();
    });

    group('Authentication State', () {
      test('should start with unauthenticated state', () {
        expect(authService.isAuthenticated, false);
        expect(authService.token, null);
        expect(authService.currentUser, null);
        expect(authService.isLoading, false);
      });

      test('should load token and user from storage on initialization', () async {
        SharedPreferences.setMockInitialValues({
          'jwt_token': 'test_token',
          'user_data': '{"username":"testuser","name":"Test User"}'
        });

        final authService = AuthService();
        await Future.delayed(Duration.zero); // Allow async initialization

        expect(authService.token, 'test_token');
        expect(authService.currentUser?.username, 'testuser');
        expect(authService.isAuthenticated, true);
        
        authService.dispose();
      });
    });

    group('Login', () {
      test('should login successfully with valid credentials', () async {
        // Mock successful login response
        when(mockHttpClient.post(
          Uri.parse('${AuthService.baseUrl}/login_check'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '{"token": "test_jwt_token"}',
          200,
        ));

        final result = await authService.login('testuser', 'password123');

        expect(result, true);
        expect(authService.isAuthenticated, true);
        expect(authService.token, 'test_jwt_token');
        expect(authService.isLoading, false);
      });

      test('should fail login with invalid credentials', () async {
        // Mock failed login response
        when(mockHttpClient.post(
          Uri.parse('${AuthService.baseUrl}/login_check'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '{"error": "Invalid credentials"}',
          401,
        ));

        final result = await authService.login('invalid', 'password');

        expect(result, false);
        expect(authService.isAuthenticated, false);
        expect(authService.token, null);
        expect(authService.isLoading, false);
      });

      test('should handle network errors during login', () async {
        // Mock network error
        when(mockHttpClient.post(
          Uri.parse('${AuthService.baseUrl}/login_check'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenThrow(Exception('Network error'));

        final result = await authService.login('testuser', 'password123');

        expect(result, false);
        expect(authService.isAuthenticated, false);
        expect(authService.isLoading, false);
      });

      test('should set loading state during login', () async {
        // Create a completer to control the async response
        when(mockHttpClient.post(
          Uri.parse('${AuthService.baseUrl}/login_check'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async {
          await Future.delayed(Duration(milliseconds: 100));
          return http.Response('{"token": "test_token"}', 200);
        });

        // Start login (don't await)
        final loginFuture = authService.login('testuser', 'password123');
        
        // Check loading state immediately
        expect(authService.isLoading, true);
        
        // Wait for completion
        await loginFuture;
        expect(authService.isLoading, false);
      });
    });

    group('Registration', () {
      test('should register successfully and auto-login', () async {
        // Mock successful registration
        when(mockHttpClient.post(
          Uri.parse('${AuthService.baseUrl}/users'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response('{"id": 1}', 201));

        // Mock successful login after registration
        when(mockHttpClient.post(
          Uri.parse('${AuthService.baseUrl}/login_check'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '{"token": "test_jwt_token"}',
          200,
        ));

        final result = await authService.register(
          'newuser', 'password123', 'password123', 'New User', 'new@example.com');

        expect(result, true);
        expect(authService.isAuthenticated, true);
        expect(authService.token, 'test_jwt_token');
      });

      test('should fail registration with invalid data', () async {
        // Mock failed registration
        when(mockHttpClient.post(
          Uri.parse('${AuthService.baseUrl}/users'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '{"error": "Validation failed"}',
          400,
        ));

        final result = await authService.register(
          'invalid', 'pass', 'different', 'User', 'invalid-email');

        expect(result, false);
        expect(authService.isAuthenticated, false);
      });
    });

    group('Logout', () {
      test('should logout and clear user data', () async {
        // Set up authenticated state
        SharedPreferences.setMockInitialValues({
          'jwt_token': 'test_token',
          'user_data': '{"username":"testuser","name":"Test User"}'
        });

        final authService = AuthService();
        await Future.delayed(Duration.zero); // Allow initialization

        // Logout
        await authService.logout();

        expect(authService.isAuthenticated, false);
        expect(authService.token, null);
        expect(authService.currentUser, null);

        authService.dispose();
      });
    });

    group('Auth Headers', () {
      test('should return headers with auth token when authenticated', () async {
        // Set up authenticated state
        SharedPreferences.setMockInitialValues({
          'jwt_token': 'test_token'
        });

        final authService = AuthService();
        await Future.delayed(Duration.zero);

        final headers = authService.getAuthHeaders();

        expect(headers['Authorization'], 'Bearer test_token');
        expect(headers['Content-Type'], 'application/json');

        authService.dispose();
      });

      test('should return basic headers when not authenticated', () {
        final headers = authService.getAuthHeaders();

        expect(headers['Authorization'], null);
        expect(headers['Content-Type'], 'application/json');
      });
    });

    group('Persistence', () {
      test('should persist auth data to storage', () async {
        SharedPreferences.setMockInitialValues({});
        
        // Mock successful login
        when(mockHttpClient.post(
          Uri.parse('${AuthService.baseUrl}/login_check'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '{"token": "persist_token"}',
          200,
        ));

        await authService.login('testuser', 'password123');

        final prefs = await SharedPreferences.getInstance();
        expect(prefs.getString('jwt_token'), 'persist_token');
      });

      test('should restore auth state from storage', () async {
        SharedPreferences.setMockInitialValues({
          'jwt_token': 'stored_token',
          'user_data': '{"username":"storeduser","name":"Stored User"}'
        });

        final newAuthService = AuthService();
        await Future.delayed(Duration.zero);

        expect(newAuthService.token, 'stored_token');
        expect(newAuthService.currentUser?.username, 'storeduser');
        expect(newAuthService.isAuthenticated, true);

        newAuthService.dispose();
      });
    });
  });
}