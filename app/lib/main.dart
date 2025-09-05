import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';

import 'services/auth_service.dart';
import 'services/api_service.dart';
import 'screens/login_screen.dart';
import 'screens/password_reset_screen.dart';
import 'screens/user_profile_screen.dart';
import 'screens/blog_list_screen.dart';
import 'screens/blog_detail_screen.dart';
import 'screens/create_post_screen.dart';
import 'widgets/main_layout.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  MyApp({super.key});

  final GoRouter _router = GoRouter(
    initialLocation: '/login',
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/password-reset',
        builder: (context, state) => const PasswordResetScreen(),
      ),
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
        ],
      ),
    ],
  );

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthService()),
        Provider(create: (_) => ApiService()),
      ],
      child: MaterialApp.router(
        title: 'SF5 Blog App',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.deepPurple,
            brightness: Brightness.light,
          ),
          useMaterial3: true,
        ),
        darkTheme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.deepPurple,
            brightness: Brightness.dark,
          ),
          useMaterial3: true,
        ),
        themeMode: ThemeMode.system, // Automatically follow system theme
        routerConfig: _router,
      ),
    );
  }
}