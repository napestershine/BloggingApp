import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';

import 'services/auth_service.dart';
import 'services/api_service.dart';
import 'services/theme_service.dart';
import 'screens/login_screen.dart';
import 'screens/password_reset_screen.dart';
import 'screens/user_profile_screen.dart';
import 'screens/blog_list_screen.dart';
import 'screens/blog_detail_screen.dart';
import 'screens/create_post_screen.dart';
import 'screens/search_screen.dart';
import 'screens/user_follow_screen.dart';
import 'screens/notifications_screen.dart';
import 'screens/bookmarks_screen.dart';
import 'widgets/main_layout.dart';

void main() {
  runApp(MyApp());
}

/// MyApp is the root widget of the BloggingApp Flutter application.
/// 
/// This widget sets up the core application structure including:
/// - Multi-provider state management for services (Auth, API, Theme)
/// - Comprehensive routing with go_router
/// - Material Design 3 theming with dynamic theme switching
/// - Global error handling and user feedback
/// 
/// The app follows a clean architecture pattern with:
/// - Services layer for business logic and data management
/// - Screens layer for UI pages
/// - Widgets layer for reusable UI components
/// 
/// Key Features:
/// - JWT-based authentication with automatic token management
/// - Dark/Light theme support with system preference detection
/// - Responsive Material Design 3 interface
/// - Comprehensive error handling with user-friendly messages
/// - Offline-capable with local storage integration
class MyApp extends StatelessWidget {
  MyApp({super.key});

  /// Application routing configuration using GoRouter
  /// 
  /// The routing is structured as follows:
  /// - Public routes: /login, /password-reset (no authentication required)
  /// - Protected routes: /blogs, /blog/:id, /create-post, /profile (authentication required)
  /// 
  /// Protected routes are wrapped in a ShellRoute with MainLayout which:
  /// - Provides consistent navigation structure
  /// - Handles authentication state checking
  /// - Shows appropriate loading and error states
  final GoRouter _router = GoRouter(
    initialLocation: '/login',
    routes: [
      // Public authentication routes
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/password-reset',
        builder: (context, state) => const PasswordResetScreen(),
      ),
      
      // Protected application routes wrapped in MainLayout
      ShellRoute(
        builder: (context, state, child) {
          return MainLayout(
            location: state.location,
            child: child,
          );
        },
        routes: [
          GoRoute(
            path: '/blogs',
            builder: (context, state) => const BlogListScreen(),
          ),
          GoRoute(
            path: '/blog/:id',
            builder: (context, state) {
              final id = int.parse(state.pathParameters['id']!);
              return BlogDetailScreen(blogId: id);
            },
          ),
          GoRoute(
            path: '/create-post',
            builder: (context, state) => const CreatePostScreen(),
          ),
          GoRoute(
            path: '/profile',
            builder: (context, state) => const UserProfileScreen(),
          ),
          GoRoute(
            path: '/search',
            builder: (context, state) => const SearchScreen(),
          ),
          GoRoute(
            path: '/user/:id/follows',
            builder: (context, state) {
              final id = int.parse(state.pathParameters['id']!);
              final username = state.queryParameters['username'] ?? 'Unknown';
              return UserFollowScreen(userId: id, username: username);
            },
          ),
          GoRoute(
            path: '/notifications',
            builder: (context, state) => const NotificationsScreen(),
          ),
          GoRoute(
            path: '/bookmarks',
            builder: (context, state) => const BookmarksScreen(),
          ),
        ],
      ),
    ],
  );

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      /// Multi-provider setup for dependency injection and state management
      /// 
      /// Services provided:
      /// - ThemeService: Manages app theming and dark/light mode switching
      /// - AuthService: Handles authentication, JWT tokens, and user session
      /// - ApiService: Manages API communication with the FastAPI backend
      /// 
      /// Using ChangeNotifierProvider for services that need to notify UI of state changes
      /// Using Provider for services that provide functionality without state changes
      providers: [
        ChangeNotifierProvider(create: (_) => ThemeService()),
        ChangeNotifierProvider(create: (_) => AuthService()),
        Provider(create: (_) => ApiService()),
      ],
      child: Consumer<ThemeService>(
        builder: (context, themeService, child) {
          return MaterialApp.router(
            title: 'SF5 Blog App',
            
            /// Light theme configuration using Material Design 3
            /// Features:
            /// - Purple color scheme for brand consistency
            /// - Material Design 3 styling with improved accessibility
            /// - Custom color schemes for better visual hierarchy
            theme: ThemeData(
              colorScheme: ColorScheme.fromSeed(
                seedColor: Colors.deepPurple,
                brightness: Brightness.light,
              ),
              useMaterial3: true,
              
              /// Enhanced button themes for better user experience
              elevatedButtonTheme: ElevatedButtonThemeData(
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(120, 48),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
              
              /// Improved input field styling
              inputDecorationTheme: InputDecorationTheme(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                filled: true,
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
              ),
              
              /// Card theme for consistent content presentation
              cardTheme: CardTheme(
                elevation: 2,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
            
            /// Dark theme configuration with matching design system
            /// Provides seamless transition between light and dark modes
            darkTheme: ThemeData(
              colorScheme: ColorScheme.fromSeed(
                seedColor: Colors.deepPurple,
                brightness: Brightness.dark,
              ),
              useMaterial3: true,
              
              /// Consistent button styling across themes
              elevatedButtonTheme: ElevatedButtonThemeData(
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(120, 48),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
              
              /// Dark theme input styling
              inputDecorationTheme: InputDecorationTheme(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                filled: true,
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
              ),
              
              /// Dark theme card styling
              cardTheme: CardTheme(
                elevation: 2,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
            
            /// Dynamic theme mode based on user preference
            /// Supports:
            /// - ThemeMode.light: Force light theme
            /// - ThemeMode.dark: Force dark theme  
            /// - ThemeMode.system: Follow system setting (default)
            themeMode: themeService.themeMode,
            
            /// Router configuration for navigation
            routerConfig: _router,
            
            /// Debug banner disabled for cleaner UI
            debugShowCheckedModeBanner: false,
          );
        },
      ),
    );
  }
}