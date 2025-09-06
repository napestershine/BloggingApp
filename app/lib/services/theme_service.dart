import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// ThemeService manages the application's theme state and provides functionality
/// for switching between light and dark modes with persistence.
/// 
/// This service follows the singleton pattern and integrates with SharedPreferences
/// to remember user's theme preference across app sessions.
/// 
/// Features:
/// - Automatic system theme detection
/// - Manual theme switching (light/dark/system)
/// - Persistent theme preference storage
/// - Real-time theme updates using ChangeNotifier
class ThemeService extends ChangeNotifier {
  static const String _themeKey = 'theme_mode';
  
  /// The current theme mode setting
  ThemeMode _themeMode = ThemeMode.system;
  
  /// Loading state indicator for async operations
  bool _isLoading = false;
  
  /// Public getter for the current theme mode
  /// Returns the active theme mode (light, dark, or system)
  ThemeMode get themeMode => _themeMode;
  
  /// Public getter for loading state
  /// Useful for showing loading indicators during theme changes
  bool get isLoading => _isLoading;
  
  /// Determines if the current theme is dark mode
  /// Takes into account both manual selection and system settings
  bool get isDarkMode {
    if (_themeMode == ThemeMode.dark) return true;
    if (_themeMode == ThemeMode.light) return false;
    
    // For system mode, check the platform brightness
    return WidgetsBinding.instance.platformDispatcher.platformBrightness == Brightness.dark;
  }
  
  /// Constructor that automatically loads saved theme preference
  ThemeService() {
    _loadThemeFromStorage();
  }
  
  /// Loads the user's theme preference from device storage
  /// This method is called automatically when the service is initialized
  /// 
  /// If no preference is saved, defaults to system theme mode
  Future<void> _loadThemeFromStorage() async {
    _isLoading = true;
    notifyListeners();
    
    try {
      final prefs = await SharedPreferences.getInstance();
      final themeModeIndex = prefs.getInt(_themeKey);
      
      if (themeModeIndex != null) {
        // Convert stored integer back to ThemeMode enum
        _themeMode = ThemeMode.values[themeModeIndex];
      }
    } catch (e) {
      // If loading fails, keep default system mode
      debugPrint('Error loading theme preference: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
  
  /// Saves the current theme preference to device storage
  /// This ensures the user's choice persists across app restarts
  Future<void> _saveThemeToStorage() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      // Store the enum index as an integer
      await prefs.setInt(_themeKey, _themeMode.index);
    } catch (e) {
      debugPrint('Error saving theme preference: $e');
    }
  }
  
  /// Changes the application theme to the specified mode
  /// 
  /// [mode] The new theme mode to apply (light, dark, or system)
  /// 
  /// This method:
  /// 1. Updates the internal theme state
  /// 2. Saves the preference to storage
  /// 3. Notifies all listeners to update the UI
  /// 
  /// Example usage:
  /// ```dart
  /// // Switch to dark mode
  /// themeService.setThemeMode(ThemeMode.dark);
  /// 
  /// // Switch to light mode
  /// themeService.setThemeMode(ThemeMode.light);
  /// 
  /// // Follow system setting
  /// themeService.setThemeMode(ThemeMode.system);
  /// ```
  Future<void> setThemeMode(ThemeMode mode) async {
    if (_themeMode == mode) return; // No change needed
    
    _themeMode = mode;
    notifyListeners(); // Update UI immediately
    
    // Save preference in background
    await _saveThemeToStorage();
  }
  
  /// Toggles between light and dark mode
  /// If currently in system mode, switches to dark mode
  /// 
  /// This is a convenience method for simple theme switching
  /// without needing to check the current state
  Future<void> toggleTheme() async {
    ThemeMode newMode;
    
    switch (_themeMode) {
      case ThemeMode.light:
        newMode = ThemeMode.dark;
        break;
      case ThemeMode.dark:
        newMode = ThemeMode.light;
        break;
      case ThemeMode.system:
        // If in system mode, toggle to opposite of current system setting
        newMode = isDarkMode ? ThemeMode.light : ThemeMode.dark;
        break;
    }
    
    await setThemeMode(newMode);
  }
  
  /// Gets a user-friendly display name for the current theme mode
  /// Useful for showing current setting in UI
  String get themeDisplayName {
    switch (_themeMode) {
      case ThemeMode.light:
        return 'Light Mode';
      case ThemeMode.dark:
        return 'Dark Mode';
      case ThemeMode.system:
        return 'System Default';
    }
  }
  
  /// Gets the appropriate icon for the current theme mode
  /// Can be used in toggle buttons or settings screens
  IconData get themeIcon {
    switch (_themeMode) {
      case ThemeMode.light:
        return Icons.light_mode;
      case ThemeMode.dark:
        return Icons.dark_mode;
      case ThemeMode.system:
        return Icons.brightness_auto;
    }
  }
}