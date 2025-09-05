import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/user.dart';

class AuthService extends ChangeNotifier {
  static const String _tokenKey = 'jwt_token';
  static const String _userKey = 'user_data';
  
  // Update this URL to match your FastAPI endpoint
  static const String baseUrl = 'http://localhost:8000';
  
  String? _token;
  User? _currentUser;
  bool _isLoading = false;

  String? get token => _token;
  User? get currentUser => _currentUser;
  bool get isAuthenticated => _token != null;
  bool get isLoading => _isLoading;

  AuthService() {
    _loadFromStorage();
  }

  Future<void> _loadFromStorage() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString(_tokenKey);
    
    final userJson = prefs.getString(_userKey);
    if (userJson != null) {
      try {
        _currentUser = User.fromJson(json.decode(userJson));
      } catch (e) {
        print('Error loading user from storage: $e');
      }
    }
    
    notifyListeners();
  }

  Future<void> _saveToStorage() async {
    final prefs = await SharedPreferences.getInstance();
    
    if (_token != null) {
      await prefs.setString(_tokenKey, _token!);
    } else {
      await prefs.remove(_tokenKey);
    }
    
    if (_currentUser != null) {
      await prefs.setString(_userKey, json.encode(_currentUser!.toJson()));
    } else {
      await prefs.remove(_userKey);
    }
  }

  Future<bool> login(String username, String password) async {
    _isLoading = true;
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'username': username,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _token = data['access_token'];
        
        // Fetch user details after successful login
        await _fetchCurrentUser();
        await _saveToStorage();
        
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        print('Login failed: ${response.statusCode} - ${response.body}');
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      print('Login error: $e');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> register(String username, String password, String retypedPassword, String name, String email) async {
    _isLoading = true;
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/register'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'username': username,
          'password': password,
          'retyped_password': retypedPassword,
          'name': name,
          'email': email,
        }),
      );

      if (response.statusCode == 201) {
        // Registration successful, now login
        _isLoading = false;
        notifyListeners();
        return await login(username, password);
      } else {
        print('Registration failed: ${response.statusCode} - ${response.body}');
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      print('Registration error: $e');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> _fetchCurrentUser() async {
    if (_token == null) return;

    try {
      // This would need to be implemented based on your API
      // For now, we'll create a basic user object
      _currentUser = const User(
        username: 'current_user',
        name: 'Current User',
      );
    } catch (e) {
      print('Error fetching current user: $e');
    }
  }

  Future<void> logout() async {
    try {
      if (_token != null) {
        // Call logout endpoint
        await http.post(
          Uri.parse('$baseUrl/auth/logout'),
          headers: getAuthHeaders(),
        );
      }
    } catch (e) {
      print('Logout API error: $e');
    } finally {
      _token = null;
      _currentUser = null;
      await _saveToStorage();
      notifyListeners();
    }
  }

  Future<bool> refreshToken() async {
    if (_token == null) return false;
    
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/refresh'),
        headers: getAuthHeaders(),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _token = data['access_token'];
        await _saveToStorage();
        notifyListeners();
        return true;
      } else {
        // Token refresh failed, logout user
        await logout();
        return false;
      }
    } catch (e) {
      print('Token refresh error: $e');
      await logout();
      return false;
    }
  }

  Map<String, String> getAuthHeaders() {
    if (_token == null) {
      return {'Content-Type': 'application/json'};
    }
    
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $_token',
    };
  }

  Future<bool> requestPasswordReset(String email) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/password/forgot'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'email': email,
        }),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Password reset request error: $e');
      return false;
    }
  }

  Future<bool> resetPassword(String token, String newPassword) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/password/reset'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'token': token,
          'new_password': newPassword,
        }),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Password reset error: $e');
      return false;
    }
  }

  Future<bool> requestEmailVerification(String email) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/verify-email'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'email': email,
        }),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Email verification request error: $e');
      return false;
    }
  }

  Future<bool> confirmEmailVerification(String token) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/verify-email/confirm'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'token': token,
        }),
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Email verification confirmation error: $e');
      return false;
    }
  }
}