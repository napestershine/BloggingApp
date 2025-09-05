import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:provider/provider.dart';
import 'package:sf5_blog_app/screens/blog_list_screen.dart';
import 'package:sf5_blog_app/services/auth_service.dart';
import 'package:sf5_blog_app/services/api_service.dart';
import 'package:sf5_blog_app/models/blog_post.dart';
import 'package:sf5_blog_app/models/user.dart';
import 'package:sf5_blog_app/widgets/blog_post_card.dart';

import 'blog_list_screen_test.mocks.dart';

@GenerateMocks([AuthService, ApiService])
void main() {
  group('BlogListScreen Widget Tests', () {
    late MockAuthService mockAuthService;
    late MockApiService mockApiService;

    setUp(() {
      mockAuthService = MockAuthService();
      mockApiService = MockApiService();
      
      // Default mock behavior
      when(mockAuthService.isAuthenticated).thenReturn(true);
      when(mockAuthService.getAuthHeaders()).thenReturn({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test_token',
      });
    });

    Widget createBlogListScreen() {
      return MaterialApp(
        home: MultiProvider(
          providers: [
            ChangeNotifierProvider<AuthService>.value(value: mockAuthService),
            Provider<ApiService>.value(value: mockApiService),
          ],
          child: const BlogListScreen(),
        ),
      );
    }

    group('Loading State', () {
      testWidgets('should show loading indicator while fetching posts', (WidgetTester tester) async {
        // Mock API call that never completes
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) => Future.delayed(const Duration(seconds: 10), () => []));

        await tester.pumpWidget(createBlogListScreen());

        // Should show loading indicator
        expect(find.byType(CircularProgressIndicator), findsOneWidget);
        expect(find.text('Loading blog posts...'), findsOneWidget);
      });

      testWidgets('should hide loading indicator after posts are loaded', (WidgetTester tester) async {
        final mockPosts = [
          BlogPost(
            id: 1,
            title: 'Test Post 1',
            content: 'Content 1',
            author: const User(username: 'author1', name: 'Author 1'),
          ),
          BlogPost(
            id: 2,
            title: 'Test Post 2',
            content: 'Content 2',
            author: const User(username: 'author2', name: 'Author 2'),
          ),
        ];

        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => mockPosts);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Loading indicator should be gone
        expect(find.byType(CircularProgressIndicator), findsNothing);
        expect(find.text('Loading blog posts...'), findsNothing);
      });
    });

    group('Blog Posts Display', () {
      testWidgets('should display list of blog posts', (WidgetTester tester) async {
        final mockPosts = [
          BlogPost(
            id: 1,
            title: 'First Post',
            content: 'First post content',
            author: const User(username: 'author1', name: 'Author 1'),
          ),
          BlogPost(
            id: 2,
            title: 'Second Post',
            content: 'Second post content',
            author: const User(username: 'author2', name: 'Author 2'),
          ),
        ];

        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => mockPosts);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Should display blog post cards
        expect(find.byType(BlogPostCard), findsNWidgets(2));
        expect(find.text('First Post'), findsOneWidget);
        expect(find.text('Second Post'), findsOneWidget);
      });

      testWidgets('should show empty state when no posts exist', (WidgetTester tester) async {
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => []);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Should show empty state
        expect(find.text('No blog posts found'), findsOneWidget);
        expect(find.text('Be the first to create a post!'), findsOneWidget);
        expect(find.byType(BlogPostCard), findsNothing);
      });

      testWidgets('should display posts in a scrollable list', (WidgetTester tester) async {
        // Create many posts to test scrolling
        final mockPosts = List.generate(20, (index) => BlogPost(
          id: index + 1,
          title: 'Post ${index + 1}',
          content: 'Content ${index + 1}',
          author: User(username: 'author$index', name: 'Author $index'),
        ));

        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => mockPosts);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Should find ListView
        expect(find.byType(ListView), findsOneWidget);
        
        // Should display first few posts
        expect(find.text('Post 1'), findsOneWidget);
        expect(find.text('Post 2'), findsOneWidget);
        
        // Scroll to see more posts
        await tester.fling(find.byType(ListView), const Offset(0, -300), 1000);
        await tester.pumpAndSettle();
        
        // Should display more posts after scrolling
        expect(find.byType(BlogPostCard), findsWidgets);
      });
    });

    group('Error Handling', () {
      testWidgets('should show error message when API call fails', (WidgetTester tester) async {
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenThrow(Exception('Network error'));

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Should show error message
        expect(find.text('Error loading blog posts'), findsOneWidget);
        expect(find.text('Network error'), findsOneWidget);
        expect(find.text('Retry'), findsOneWidget);
      });

      testWidgets('should retry loading posts when retry button is tapped', (WidgetTester tester) async {
        // First call fails
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenThrow(Exception('Network error'));

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Should show error state
        expect(find.text('Retry'), findsOneWidget);

        // Setup successful retry
        final mockPosts = [
          BlogPost(
            id: 1,
            title: 'Retry Post',
            content: 'This post loaded after retry',
          ),
        ];

        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => mockPosts);

        // Tap retry button
        await tester.tap(find.text('Retry'));
        await tester.pumpAndSettle();

        // Should show posts after successful retry
        expect(find.text('Retry Post'), findsOneWidget);
        expect(find.text('Error loading blog posts'), findsNothing);
      });
    });

    group('App Bar', () {
      testWidgets('should display app bar with title', (WidgetTester tester) async {
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => []);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        expect(find.byType(AppBar), findsOneWidget);
        expect(find.text('Blog Posts'), findsOneWidget);
      });

      testWidgets('should have create post action button', (WidgetTester tester) async {
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => []);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Should have add/create button in app bar
        expect(find.byIcon(Icons.add), findsOneWidget);
      });

      testWidgets('should have logout action', (WidgetTester tester) async {
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => []);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Should have logout option (could be in menu or as direct button)
        expect(find.byIcon(Icons.logout), findsOneWidget);
      });
    });

    group('Navigation', () {
      testWidgets('should navigate to create post screen when add button is tapped', (WidgetTester tester) async {
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => []);

        await tester.pumpWidget(
          MaterialApp(
            initialRoute: '/blogs',
            routes: {
              '/blogs': (context) => MultiProvider(
                providers: [
                  ChangeNotifierProvider<AuthService>.value(value: mockAuthService),
                  Provider<ApiService>.value(value: mockApiService),
                ],
                child: const BlogListScreen(),
              ),
              '/create-post': (context) => const Scaffold(body: Text('Create Post Screen')),
            },
          ),
        );
        await tester.pumpAndSettle();

        // Tap create post button
        await tester.tap(find.byIcon(Icons.add));
        await tester.pumpAndSettle();

        // Should navigate to create post screen
        expect(find.text('Create Post Screen'), findsOneWidget);
      });

      testWidgets('should navigate to post detail when post is tapped', (WidgetTester tester) async {
        final mockPosts = [
          BlogPost(
            id: 1,
            title: 'Tappable Post',
            content: 'This post should be tappable',
          ),
        ];

        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => mockPosts);

        await tester.pumpWidget(
          MaterialApp(
            initialRoute: '/blogs',
            routes: {
              '/blogs': (context) => MultiProvider(
                providers: [
                  ChangeNotifierProvider<AuthService>.value(value: mockAuthService),
                  Provider<ApiService>.value(value: mockApiService),
                ],
                child: const BlogListScreen(),
              ),
              '/blog/1': (context) => const Scaffold(body: Text('Blog Detail Screen')),
            },
          ),
        );
        await tester.pumpAndSettle();

        // Tap on blog post card
        await tester.tap(find.byType(BlogPostCard));
        await tester.pumpAndSettle();

        // Should navigate to blog detail
        expect(find.text('Blog Detail Screen'), findsOneWidget);
      });
    });

    group('Authentication', () {
      testWidgets('should use auth headers for API calls', (WidgetTester tester) async {
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => []);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Verify API was called with auth headers
        verify(mockApiService.getBlogPosts(headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test_token',
        })).called(1);
      });

      testWidgets('should handle logout when logout button is tapped', (WidgetTester tester) async {
        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => []);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Tap logout button
        await tester.tap(find.byIcon(Icons.logout));
        await tester.pumpAndSettle();

        // Should call logout on auth service
        verify(mockAuthService.logout()).called(1);
      });
    });

    group('Pull to Refresh', () {
      testWidgets('should support pull to refresh', (WidgetTester tester) async {
        final mockPosts = [
          BlogPost(id: 1, title: 'Initial Post', content: 'Initial content'),
        ];

        when(mockApiService.getBlogPosts(headers: anyNamed('headers')))
            .thenAnswer((_) async => mockPosts);

        await tester.pumpWidget(createBlogListScreen());
        await tester.pumpAndSettle();

        // Should have RefreshIndicator
        expect(find.byType(RefreshIndicator), findsOneWidget);

        // Perform pull to refresh
        await tester.fling(find.byType(ListView), const Offset(0, 300), 1000);
        await tester.pump();
        await tester.pump(const Duration(seconds: 1));

        // API should be called again
        verify(mockApiService.getBlogPosts(headers: anyNamed('headers'))).called(2);
      });
    });
  });
}