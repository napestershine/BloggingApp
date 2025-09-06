import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/theme_service.dart';

/// ThemeToggleButton provides a user interface for switching between
/// light, dark, and system theme modes.
/// 
/// This widget creates an intuitive toggle button that cycles through
/// theme modes and provides visual feedback about the current selection.
/// It integrates seamlessly with the ThemeService to persist user preferences.
/// 
/// Features:
/// - Visual icon representation of current theme mode
/// - Smooth animations between theme changes
/// - Tooltip showing current theme mode
/// - Accessibility support with semantic labels
/// - Consistent styling that adapts to current theme
/// 
/// The button cycles through modes in this order:
/// System → Light → Dark → System
/// 
/// Usage:
/// ```dart
/// // In app bar actions
/// AppBar(
///   actions: [
///     ThemeToggleButton(),
///   ],
/// )
/// 
/// // In settings screen
/// ListTile(
///   title: Text('Theme'),
///   trailing: ThemeToggleButton(),
/// )
/// ```
class ThemeToggleButton extends StatelessWidget {
  /// Creates a theme toggle button
  /// 
  /// [onThemeChanged] Optional callback when theme changes
  /// [size] Size of the icon button (default: 24.0)
  /// [showTooltip] Whether to show tooltip on hover (default: true)
  const ThemeToggleButton({
    super.key,
    this.onThemeChanged,
    this.size = 24.0,
    this.showTooltip = true,
  });

  /// Optional callback function called when theme changes
  final VoidCallback? onThemeChanged;

  /// Size of the icon in the button
  final double size;

  /// Whether to show tooltip with current theme mode
  final bool showTooltip;

  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeService>(
      builder: (context, themeService, child) {
        return IconButton(
          /// Tooltip showing current theme mode and next action
          tooltip: showTooltip ? _getTooltipText(themeService.themeMode) : null,
          
          /// Icon representing current theme mode
          icon: AnimatedSwitcher(
            duration: const Duration(milliseconds: 300),
            transitionBuilder: (Widget child, Animation<double> animation) {
              return RotationTransition(
                turns: animation,
                child: child,
              );
            },
            child: Icon(
              themeService.themeIcon,
              key: ValueKey(themeService.themeMode),
              size: size,
            ),
          ),
          
          /// Theme toggle action
          onPressed: themeService.isLoading
              ? null // Disable while loading
              : () async {
                  await _toggleTheme(context, themeService);
                  onThemeChanged?.call();
                },
          
          /// Visual styling
          style: IconButton.styleFrom(
            backgroundColor: Theme.of(context).colorScheme.surfaceVariant.withOpacity(0.1),
            foregroundColor: Theme.of(context).colorScheme.onSurface,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        );
      },
    );
  }

  /// Handles theme toggle logic with user feedback
  Future<void> _toggleTheme(BuildContext context, ThemeService themeService) async {
    final oldMode = themeService.themeMode;
    
    try {
      await themeService.toggleTheme();
      
      // Show brief feedback to user
      if (context.mounted) {
        ScaffoldMessenger.of(context).removeCurrentSnackBar();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Theme changed to ${themeService.themeDisplayName}',
              style: const TextStyle(fontSize: 14),
            ),
            duration: const Duration(seconds: 1),
            behavior: SnackBarBehavior.floating,
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        );
      }
    } catch (e) {
      // If theme change fails, show error and optionally revert
      debugPrint('Theme toggle error: $e');
      
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: const Text('Failed to change theme'),
            backgroundColor: Theme.of(context).colorScheme.error,
            action: SnackBarAction(
              label: 'Retry',
              onPressed: () => _toggleTheme(context, themeService),
            ),
          ),
        );
      }
    }
  }

  /// Gets appropriate tooltip text based on current theme mode
  String _getTooltipText(ThemeMode currentMode) {
    switch (currentMode) {
      case ThemeMode.system:
        return 'Current: System Default\nTap to switch to Light Mode';
      case ThemeMode.light:
        return 'Current: Light Mode\nTap to switch to Dark Mode';
      case ThemeMode.dark:
        return 'Current: Dark Mode\nTap to switch to System Default';
    }
  }
}

/// ThemeSelector provides a more comprehensive theme selection interface
/// with radio buttons for each theme mode.
/// 
/// This widget is ideal for settings screens where users need
/// explicit control over theme selection.
class ThemeSelector extends StatelessWidget {
  /// Creates a theme selector with radio buttons
  /// 
  /// [onThemeChanged] Optional callback when theme changes
  /// [showLabels] Whether to show text labels (default: true)
  const ThemeSelector({
    super.key,
    this.onThemeChanged,
    this.showLabels = true,
  });

  /// Optional callback function called when theme changes
  final VoidCallback? onThemeChanged;

  /// Whether to show text labels next to radio buttons
  final bool showLabels;

  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeService>(
      builder: (context, themeService, child) {
        return Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (showLabels)
              Text(
                'Theme Mode',
                style: Theme.of(context).textTheme.titleMedium,
              ),
            if (showLabels) const SizedBox(height: 8),
            
            /// System theme option
            RadioListTile<ThemeMode>(
              title: showLabels ? const Text('System Default') : null,
              subtitle: showLabels 
                  ? const Text('Follow device setting')
                  : null,
              secondary: const Icon(Icons.brightness_auto),
              value: ThemeMode.system,
              groupValue: themeService.themeMode,
              onChanged: themeService.isLoading
                  ? null
                  : (ThemeMode? value) async {
                      if (value != null) {
                        await themeService.setThemeMode(value);
                        onThemeChanged?.call();
                      }
                    },
            ),
            
            /// Light theme option
            RadioListTile<ThemeMode>(
              title: showLabels ? const Text('Light Mode') : null,
              subtitle: showLabels 
                  ? const Text('Always use light theme')
                  : null,
              secondary: const Icon(Icons.light_mode),
              value: ThemeMode.light,
              groupValue: themeService.themeMode,
              onChanged: themeService.isLoading
                  ? null
                  : (ThemeMode? value) async {
                      if (value != null) {
                        await themeService.setThemeMode(value);
                        onThemeChanged?.call();
                      }
                    },
            ),
            
            /// Dark theme option
            RadioListTile<ThemeMode>(
              title: showLabels ? const Text('Dark Mode') : null,
              subtitle: showLabels 
                  ? const Text('Always use dark theme')
                  : null,
              secondary: const Icon(Icons.dark_mode),
              value: ThemeMode.dark,
              groupValue: themeService.themeMode,
              onChanged: themeService.isLoading
                  ? null
                  : (ThemeMode? value) async {
                      if (value != null) {
                        await themeService.setThemeMode(value);
                        onThemeChanged?.call();
                      }
                    },
            ),
          ],
        );
      },
    );
  }
}