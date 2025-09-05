import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:sf5_blog_app/services/auth_service.dart';
import 'package:sf5_blog_app/services/api_service.dart';

/// Helper function to create a test app with necessary providers
Widget createTestApp({
  required Widget child,
  AuthService? authService,
  ApiService? apiService,
}) {
  return MultiProvider(
    providers: [
      ChangeNotifierProvider<AuthService>.value(
        value: authService ?? MockAuthService(),
      ),
      Provider<ApiService>.value(
        value: apiService ?? MockApiService(),
      ),
    ],
    child: MaterialApp(
      home: child,
    ),
  );
}

/// Helper function to create a test app with routing
Widget createTestAppWithRouting({
  required Map<String, WidgetBuilder> routes,
  required String initialRoute,
  AuthService? authService,
  ApiService? apiService,
}) {
  return MultiProvider(
    providers: [
      ChangeNotifierProvider<AuthService>.value(
        value: authService ?? MockAuthService(),
      ),
      Provider<ApiService>.value(
        value: apiService ?? MockApiService(),
      ),
    ],
    child: MaterialApp(
      initialRoute: initialRoute,
      routes: routes,
    ),
  );
}

/// Mock implementation for testing
class MockAuthService extends AuthService {
  bool _isAuthenticated = false;
  bool _isLoading = false;
  String? _token;
  
  @override
  bool get isAuthenticated => _isAuthenticated;
  
  @override
  bool get isLoading => _isLoading;
  
  @override
  String? get token => _token;
  
  void setAuthenticated(bool value) {
    _isAuthenticated = value;
    notifyListeners();
  }
  
  void setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }
  
  void setToken(String? value) {
    _token = value;
    notifyListeners();
  }
  
  @override
  Future<bool> login(String username, String password) async {
    _isLoading = true;
    notifyListeners();
    
    await Future.delayed(const Duration(milliseconds: 100));
    
    // Mock successful login for specific credentials
    if (username == 'testuser' && password == 'password123') {
      _isAuthenticated = true;
      _token = 'mock_token';
    }
    
    _isLoading = false;
    notifyListeners();
    
    return _isAuthenticated;
  }
  
  @override
  Future<bool> register(String username, String password, String retypedPassword,
      String name, String email) async {
    _isLoading = true;
    notifyListeners();
    
    await Future.delayed(const Duration(milliseconds: 100));
    
    // Mock successful registration
    _isAuthenticated = true;
    _token = 'mock_token';
    
    _isLoading = false;
    notifyListeners();
    
    return true;
  }
  
  @override
  Future<void> logout() async {
    _isAuthenticated = false;
    _token = null;
    notifyListeners();
  }
  
  @override
  Map<String, String> getAuthHeaders() {
    return {
      'Content-Type': 'application/json',
      if (_token != null) 'Authorization': 'Bearer $_token',
    };
  }
}

/// Mock implementation for testing
class MockApiService extends ApiService {
  // This would contain mock implementations of API methods
  // for use in widget tests where we don't want real network calls
}