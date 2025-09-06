import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'dart:io';

/// ErrorService provides comprehensive error handling and user-friendly messaging
/// for the BloggingApp Flutter application.
/// 
/// This service centralizes error handling logic and provides consistent
/// user feedback across the entire application. It categorizes different
/// types of errors and provides appropriate user-friendly messages.
/// 
/// Features:
/// - HTTP error code handling with user-friendly messages
/// - Network connectivity error detection
/// - Authentication error handling
/// - Validation error processing
/// - Consistent snackbar notifications
/// - Error logging for debugging
/// 
/// Usage:
/// ```dart
/// // Handle an HTTP error response
/// ErrorService.handleHttpError(context, response);
/// 
/// // Handle a general exception
/// ErrorService.handleException(context, exception);
/// 
/// // Show a custom error message
/// ErrorService.showError(context, 'Custom error message');
/// ```
class ErrorService {
  /// Private constructor to prevent instantiation (utility class)
  ErrorService._();
  
  /// Default error message when no specific message is available
  static const String defaultErrorMessage = 'Something went wrong. Please try again.';
  
  /// Error message for network connectivity issues
  static const String networkErrorMessage = 'Please check your internet connection and try again.';
  
  /// Error message for server unavailability
  static const String serverErrorMessage = 'Server is temporarily unavailable. Please try again later.';
  
  /// Error message for authentication failures
  static const String authErrorMessage = 'Authentication failed. Please check your credentials.';
  
  /// Error message for permission denied errors
  static const String permissionErrorMessage = 'You don\'t have permission to perform this action.';
  
  /// Error message for validation failures
  static const String validationErrorMessage = 'Please check your input and try again.';
  
  /// Handles HTTP response errors and shows appropriate user feedback
  /// 
  /// [context] BuildContext for showing snackbars
  /// [statusCode] HTTP status code from the response
  /// [responseBody] Optional response body for additional error details
  /// [customMessage] Optional custom message to override default messages
  /// 
  /// This method maps HTTP status codes to user-friendly messages:
  /// - 400: Bad Request (validation errors)
  /// - 401: Unauthorized (authentication required)
  /// - 403: Forbidden (insufficient permissions)
  /// - 404: Not Found (resource doesn't exist)
  /// - 409: Conflict (duplicate data)
  /// - 422: Unprocessable Entity (validation errors)
  /// - 429: Too Many Requests (rate limiting)
  /// - 500+: Server errors
  static void handleHttpError(
    BuildContext context,
    int statusCode, {
    String? responseBody,
    String? customMessage,
  }) {
    String message = customMessage ?? _getHttpErrorMessage(statusCode);
    
    // Log error for debugging (in debug mode only)
    if (kDebugMode) {
      debugPrint('HTTP Error $statusCode: $message');
      if (responseBody != null) {
        debugPrint('Response body: $responseBody');
      }
    }
    
    // Parse response body for more specific error messages
    String? specificMessage = _parseErrorFromResponse(responseBody);
    if (specificMessage != null) {
      message = specificMessage;
    }
    
    _showErrorSnackbar(context, message, _getErrorColor(statusCode));
  }
  
  /// Handles general exceptions and provides user-friendly feedback
  /// 
  /// [context] BuildContext for showing snackbars
  /// [exception] The exception that occurred
  /// [customMessage] Optional custom message to show to user
  /// [retryAction] Optional callback for retry functionality
  /// 
  /// This method categorizes exceptions and provides appropriate messages:
  /// - SocketException: Network connectivity issues
  /// - TimeoutException: Request timeouts
  /// - FormatException: Data parsing errors
  /// - ArgumentError: Invalid input data
  static void handleException(
    BuildContext context,
    dynamic exception, {
    String? customMessage,
    VoidCallback? retryAction,
  }) {
    String message = customMessage ?? _getExceptionMessage(exception);
    
    // Log exception for debugging
    if (kDebugMode) {
      debugPrint('Exception: ${exception.toString()}');
      debugPrint('Stack trace: ${StackTrace.current}');
    }
    
    _showErrorSnackbar(
      context, 
      message, 
      Colors.red,
      retryAction: retryAction,
    );
  }
  
  /// Shows a simple error message to the user
  /// 
  /// [context] BuildContext for showing snackbars
  /// [message] Error message to display
  /// [duration] How long to show the message (default: 4 seconds)
  static void showError(
    BuildContext context,
    String message, {
    Duration duration = const Duration(seconds: 4),
  }) {
    _showErrorSnackbar(context, message, Colors.red, duration: duration);
  }
  
  /// Shows a warning message to the user
  /// 
  /// [context] BuildContext for showing snackbars
  /// [message] Warning message to display
  /// [duration] How long to show the message (default: 3 seconds)
  static void showWarning(
    BuildContext context,
    String message, {
    Duration duration = const Duration(seconds: 3),
  }) {
    _showErrorSnackbar(context, message, Colors.orange, duration: duration);
  }
  
  /// Shows a success message to the user
  /// 
  /// [context] BuildContext for showing snackbars
  /// [message] Success message to display
  /// [duration] How long to show the message (default: 2 seconds)
  static void showSuccess(
    BuildContext context,
    String message, {
    Duration duration = const Duration(seconds: 2),
  }) {
    _showErrorSnackbar(context, message, Colors.green, duration: duration);
  }
  
  /// Shows an info message to the user
  /// 
  /// [context] BuildContext for showing snackbars
  /// [message] Info message to display
  /// [duration] How long to show the message (default: 3 seconds)
  static void showInfo(
    BuildContext context,
    String message, {
    Duration duration = const Duration(seconds: 3),
  }) {
    _showErrorSnackbar(context, message, Colors.blue, duration: duration);
  }
  
  /// Internal method to show a snackbar with consistent styling
  static void _showErrorSnackbar(
    BuildContext context,
    String message,
    Color backgroundColor, {
    Duration duration = const Duration(seconds: 4),
    VoidCallback? retryAction,
  }) {
    // Remove any existing snackbars to avoid stacking
    ScaffoldMessenger.of(context).removeCurrentSnackBar();
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          message,
          style: const TextStyle(color: Colors.white),
        ),
        backgroundColor: backgroundColor,
        duration: duration,
        behavior: SnackBarBehavior.floating,
        action: retryAction != null
            ? SnackBarAction(
                label: 'Retry',
                textColor: Colors.white,
                onPressed: retryAction,
              )
            : null,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
  }
  
  /// Maps HTTP status codes to user-friendly error messages
  static String _getHttpErrorMessage(int statusCode) {
    switch (statusCode) {
      case 400:
        return validationErrorMessage;
      case 401:
        return authErrorMessage;
      case 403:
        return permissionErrorMessage;
      case 404:
        return 'The requested resource was not found.';
      case 409:
        return 'This data already exists. Please use different values.';
      case 422:
        return validationErrorMessage;
      case 429:
        return 'Too many requests. Please wait a moment and try again.';
      case 500:
      case 502:
      case 503:
      case 504:
        return serverErrorMessage;
      default:
        if (statusCode >= 500) {
          return serverErrorMessage;
        } else if (statusCode >= 400) {
          return 'Request failed. Please check your input and try again.';
        }
        return defaultErrorMessage;
    }
  }
  
  /// Determines the appropriate color for error messages based on HTTP status code
  static Color _getErrorColor(int statusCode) {
    if (statusCode >= 500) {
      return Colors.red; // Server errors - critical
    } else if (statusCode == 401 || statusCode == 403) {
      return Colors.orange; // Auth errors - warning
    } else if (statusCode >= 400) {
      return Colors.amber; // Client errors - caution
    }
    return Colors.red; // Default error color
  }
  
  /// Maps exceptions to user-friendly messages
  static String _getExceptionMessage(dynamic exception) {
    if (exception is SocketException) {
      return networkErrorMessage;
    } else if (exception is TimeoutException) {
      return 'Request timed out. Please check your connection and try again.';
    } else if (exception is FormatException) {
      return 'Invalid data received. Please try again.';
    } else if (exception is ArgumentError) {
      return validationErrorMessage;
    } else if (exception.toString().contains('Connection refused')) {
      return 'Cannot connect to server. Please try again later.';
    } else if (exception.toString().contains('No route to host')) {
      return networkErrorMessage;
    }
    
    return defaultErrorMessage;
  }
  
  /// Attempts to parse specific error messages from API response body
  static String? _parseErrorFromResponse(String? responseBody) {
    if (responseBody == null || responseBody.isEmpty) return null;
    
    try {
      // Try to parse JSON response for detailed error messages
      // This would depend on your API's error response format
      // Example: {"detail": "Username already exists"}
      final response = responseBody.toLowerCase();
      
      if (response.contains('username') && response.contains('already')) {
        return 'This username is already taken. Please choose another.';
      } else if (response.contains('email') && response.contains('already')) {
        return 'This email is already registered. Please use another email.';
      } else if (response.contains('password') && response.contains('match')) {
        return 'Passwords do not match. Please check and try again.';
      } else if (response.contains('invalid') && response.contains('credentials')) {
        return 'Invalid username or password. Please check and try again.';
      } else if (response.contains('token') && response.contains('expired')) {
        return 'Your session has expired. Please log in again.';
      }
    } catch (e) {
      // If parsing fails, return null to use default message
      debugPrint('Error parsing response body: $e');
    }
    
    return null;
  }
  
  /// Validates form input and returns user-friendly error messages
  /// 
  /// [field] The name of the field being validated
  /// [value] The value to validate
  /// [rules] Validation rules to apply
  /// 
  /// Returns null if validation passes, error message if validation fails
  static String? validateField(String field, String? value, List<String> rules) {
    if (value == null || value.trim().isEmpty) {
      if (rules.contains('required')) {
        return '${field.capitalizeFirst()} is required.';
      }
      return null;
    }
    
    final trimmedValue = value.trim();
    
    // Email validation
    if (rules.contains('email')) {
      final emailRegex = RegExp(r'^[^@]+@[^@]+\.[^@]+$');
      if (!emailRegex.hasMatch(trimmedValue)) {
        return 'Please enter a valid email address.';
      }
    }
    
    // Minimum length validation
    for (String rule in rules) {
      if (rule.startsWith('min:')) {
        final minLength = int.tryParse(rule.split(':')[1]);
        if (minLength != null && trimmedValue.length < minLength) {
          return '${field.capitalizeFirst()} must be at least $minLength characters long.';
        }
      }
    }
    
    // Maximum length validation
    for (String rule in rules) {
      if (rule.startsWith('max:')) {
        final maxLength = int.tryParse(rule.split(':')[1]);
        if (maxLength != null && trimmedValue.length > maxLength) {
          return '${field.capitalizeFirst()} must be no more than $maxLength characters long.';
        }
      }
    }
    
    // Password strength validation
    if (rules.contains('strong_password')) {
      if (trimmedValue.length < 8) {
        return 'Password must be at least 8 characters long.';
      }
      if (!RegExp(r'[A-Z]').hasMatch(trimmedValue)) {
        return 'Password must contain at least one uppercase letter.';
      }
      if (!RegExp(r'[a-z]').hasMatch(trimmedValue)) {
        return 'Password must contain at least one lowercase letter.';
      }
      if (!RegExp(r'[0-9]').hasMatch(trimmedValue)) {
        return 'Password must contain at least one number.';
      }
    }
    
    return null;
  }
}

/// Extension to capitalize the first letter of a string
extension StringExtension on String {
  String capitalizeFirst() {
    if (isEmpty) return this;
    return this[0].toUpperCase() + substring(1);
  }
}

/// TimeoutException class for handling timeouts
class TimeoutException implements Exception {
  final String message;
  const TimeoutException(this.message);
  
  @override
  String toString() => 'TimeoutException: $message';
}