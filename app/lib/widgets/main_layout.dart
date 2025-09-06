import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../widgets/theme_toggle_button.dart';

/// MainLayout provides the core navigation structure for authenticated users.
/// 
/// This widget wraps all protected screens and provides:
/// - Consistent navigation with AppBar and BottomNavigationBar
/// - Theme toggle functionality in the app bar
/// - User logout capability
/// - Automatic navigation state management based on current route
/// 
/// The layout adapts to different screen sizes and provides
/// intuitive navigation between core app features:
/// - Blog browsing and reading
/// - Content creation
/// - User profile management
/// 
/// Features:
/// - Material Design 3 navigation components
/// - Smooth transitions between screens
/// - Theme toggle integration
/// - Logout functionality with confirmation
/// - Responsive design for various screen sizes
class MainLayout extends StatefulWidget {
  final Widget child;
  final String location;

  const MainLayout({
    super.key,
    required this.child,
    required this.location,
  });

  @override
  State<MainLayout> createState() => _MainLayoutState();
}

class _MainLayoutState extends State<MainLayout> {
  int _currentIndex = 0;

  final List<NavigationItem> _navigationItems = [
    NavigationItem(
      icon: Icons.article,
      label: 'Blogs',
      route: '/blogs',
    ),
    NavigationItem(
      icon: Icons.search,
      label: 'Search',
      route: '/search',
    ),
    NavigationItem(
      icon: Icons.bookmark,
      label: 'Bookmarks',
      route: '/bookmarks',
    ),
    NavigationItem(
      icon: Icons.notifications,
      label: 'Notifications',
      route: '/notifications',
    ),
    NavigationItem(
      icon: Icons.person,
      label: 'Profile',
      route: '/profile',
    ),
  ];

  @override
  void initState() {
    super.initState();
    _updateCurrentIndex();
  }

  @override
  void didUpdateWidget(MainLayout oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.location != widget.location) {
      _updateCurrentIndex();
    }
  }

  void _updateCurrentIndex() {
    for (int i = 0; i < _navigationItems.length; i++) {
      if (widget.location.startsWith(_navigationItems[i].route)) {
        setState(() {
          _currentIndex = i;
        });
        break;
      }
    }
  }

  void _onItemTapped(int index) {
    if (index != _currentIndex) {
      context.go(_navigationItems[index].route);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      /// App bar with theme toggle and logout functionality
      appBar: AppBar(
        title: Text(_getPageTitle()),
        backgroundColor: Theme.of(context).colorScheme.surface,
        foregroundColor: Theme.of(context).colorScheme.onSurface,
        elevation: 0,
        actions: [
          // Create post button
          if (!widget.location.startsWith('/create-post'))
            IconButton(
              onPressed: () => context.go('/create-post'),
              icon: const Icon(Icons.create),
              tooltip: 'Create Post',
            ),
          
          // Theme toggle button
          const ThemeToggleButton(),
          
          // Logout button
          IconButton(
            onPressed: () => _showLogoutDialog(context),
            icon: const Icon(Icons.logout),
            tooltip: 'Logout',
          ),
        ],
      ),
      
      /// Main content area
      body: widget.child,
      
      /// Bottom navigation for primary app sections
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: _onItemTapped,
        type: BottomNavigationBarType.fixed,
        backgroundColor: Theme.of(context).colorScheme.surface,
        selectedItemColor: Theme.of(context).colorScheme.primary,
        unselectedItemColor: Theme.of(context).colorScheme.onSurface.withOpacity(0.6),
        items: _navigationItems
            .map((item) => BottomNavigationBarItem(
                  icon: Icon(item.icon),
                  label: item.label,
                ))
            .toList(),
      ),
    );
  }

  /// Gets the appropriate page title based on current route
  String _getPageTitle() {
    if (widget.location.startsWith('/blogs')) {
      return 'Blog Posts';
    } else if (widget.location.startsWith('/blog/')) {
      return 'Blog Details';
    } else if (widget.location.startsWith('/search')) {
      return 'Search';
    } else if (widget.location.startsWith('/bookmarks')) {
      return 'Bookmarks';
    } else if (widget.location.startsWith('/notifications')) {
      return 'Notifications';
    } else if (widget.location.startsWith('/user/') && widget.location.contains('/follows')) {
      return 'User Network';
    } else if (widget.location.startsWith('/create-post')) {
      return 'Create Post';
    } else if (widget.location.startsWith('/profile')) {
      return 'Profile';
    }
    return 'BloggingApp';
  }

  /// Shows logout confirmation dialog
  void _showLogoutDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Logout'),
          content: const Text('Are you sure you want to logout?'),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                Navigator.of(context).pop();
                await _performLogout(context);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Theme.of(context).colorScheme.error,
                foregroundColor: Theme.of(context).colorScheme.onError,
              ),
              child: const Text('Logout'),
            ),
          ],
        );
      },
    );
  }

  /// Performs the logout operation
  Future<void> _performLogout(BuildContext context) async {
    try {
      final authService = Provider.of<AuthService>(context, listen: false);
      await authService.logout();
      
      if (context.mounted) {
        context.go('/login');
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Successfully logged out'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Logout failed: ${e.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }
}

class NavigationItem {
  final IconData icon;
  final String label;
  final String route;

  NavigationItem({
    required this.icon,
    required this.label,
    required this.route,
  });
}