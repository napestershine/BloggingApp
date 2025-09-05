import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:http/http.dart' as http;
import 'package:sf5_blog_app/services/api_service.dart';
import 'package:sf5_blog_app/models/blog_post.dart';
import 'package:sf5_blog_app/models/comment.dart';
import 'package:sf5_blog_app/models/user.dart';

import 'api_service_test.mocks.dart';

@GenerateMocks([http.Client])
void main() {
  group('ApiService Tests', () {
    late ApiService apiService;
    late MockClient mockHttpClient;

    setUp(() {
      mockHttpClient = MockClient();
      apiService = ApiService();
    });

    group('Blog Posts', () {
      test('should fetch blog posts successfully', () async {
        // Mock successful response
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response(
          '''
          {
            "hydra:member": [
              {
                "id": 1,
                "title": "Test Post 1",
                "content": "Content 1",
                "slug": "test-post-1",
                "published": "2024-01-01T00:00:00Z"
              },
              {
                "id": 2,
                "title": "Test Post 2",
                "content": "Content 2",
                "slug": "test-post-2",
                "published": "2024-01-02T00:00:00Z"
              }
            ]
          }
          ''',
          200,
        ));

        final posts = await apiService.getBlogPosts();

        expect(posts, hasLength(2));
        expect(posts[0].title, 'Test Post 1');
        expect(posts[1].title, 'Test Post 2');
      });

      test('should handle API error when fetching blog posts', () async {
        // Mock error response
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response(
          '{"error": "Server error"}',
          500,
        ));

        expect(
          () => apiService.getBlogPosts(),
          throwsA(isA<Exception>()),
        );
      });

      test('should handle network error when fetching blog posts', () async {
        // Mock network error
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: anyNamed('headers'),
        )).thenThrow(Exception('Network error'));

        expect(
          () => apiService.getBlogPosts(),
          throwsA(isA<Exception>()),
        );
      });

      test('should fetch single blog post successfully', () async {
        // Mock successful response
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts/1'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response(
          '''
          {
            "id": 1,
            "title": "Test Post",
            "content": "Test Content",
            "slug": "test-post",
            "published": "2024-01-01T00:00:00Z"
          }
          ''',
          200,
        ));

        final post = await apiService.getBlogPost(1);

        expect(post.id, 1);
        expect(post.title, 'Test Post');
        expect(post.content, 'Test Content');
      });

      test('should create blog post successfully', () async {
        final newPost = BlogPost(
          title: 'New Post',
          content: 'New Content',
          slug: 'new-post',
        );

        // Mock successful response
        when(mockHttpClient.post(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '''
          {
            "id": 1,
            "title": "New Post",
            "content": "New Content",
            "slug": "new-post",
            "published": "2024-01-01T00:00:00Z"
          }
          ''',
          201,
        ));

        final createdPost = await apiService.createBlogPost(newPost);

        expect(createdPost.id, 1);
        expect(createdPost.title, 'New Post');
      });

      test('should handle creation error', () async {
        final newPost = BlogPost(
          title: 'Invalid Post',
          content: '',
          slug: '',
        );

        // Mock error response
        when(mockHttpClient.post(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '{"error": "Validation failed"}',
          400,
        ));

        expect(
          () => apiService.createBlogPost(newPost),
          throwsA(isA<Exception>()),
        );
      });

      test('should update blog post successfully', () async {
        final updatedPost = BlogPost(
          id: 1,
          title: 'Updated Post',
          content: 'Updated Content',
          slug: 'updated-post',
        );

        // Mock successful response
        when(mockHttpClient.put(
          Uri.parse('${ApiService.baseUrl}/blog_posts/1'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '''
          {
            "id": 1,
            "title": "Updated Post",
            "content": "Updated Content",
            "slug": "updated-post",
            "published": "2024-01-01T00:00:00Z"
          }
          ''',
          200,
        ));

        final result = await apiService.updateBlogPost(1, updatedPost);

        expect(result.title, 'Updated Post');
        expect(result.content, 'Updated Content');
      });

      test('should delete blog post successfully', () async {
        // Mock successful deletion
        when(mockHttpClient.delete(
          Uri.parse('${ApiService.baseUrl}/blog_posts/1'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response('', 204));

        // Should not throw an exception
        await apiService.deleteBlogPost(1);
      });

      test('should handle deletion error', () async {
        // Mock error response
        when(mockHttpClient.delete(
          Uri.parse('${ApiService.baseUrl}/blog_posts/1'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response(
          '{"error": "Not found"}',
          404,
        ));

        expect(
          () => apiService.deleteBlogPost(1),
          throwsA(isA<Exception>()),
        );
      });
    });

    group('Comments', () {
      test('should fetch all comments successfully', () async {
        // Mock successful response
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/comments'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response(
          '''
          {
            "hydra:member": [
              {
                "id": 1,
                "content": "Comment 1",
                "published": "2024-01-01T00:00:00Z"
              },
              {
                "id": 2,
                "content": "Comment 2",
                "published": "2024-01-02T00:00:00Z"
              }
            ]
          }
          ''',
          200,
        ));

        final comments = await apiService.getComments();

        expect(comments, hasLength(2));
        expect(comments[0].content, 'Comment 1');
        expect(comments[1].content, 'Comment 2');
      });

      test('should fetch blog post comments successfully', () async {
        // Mock successful response
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts/1/comments'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response(
          '''
          {
            "hydra:member": [
              {
                "id": 1,
                "content": "Blog post comment",
                "published": "2024-01-01T00:00:00Z"
              }
            ]
          }
          ''',
          200,
        ));

        final comments = await apiService.getBlogPostComments(1);

        expect(comments, hasLength(1));
        expect(comments[0].content, 'Blog post comment');
      });

      test('should create comment successfully', () async {
        final newComment = Comment(content: 'New comment');

        // Mock successful response
        when(mockHttpClient.post(
          Uri.parse('${ApiService.baseUrl}/comments'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '''
          {
            "id": 1,
            "content": "New comment",
            "published": "2024-01-01T00:00:00Z"
          }
          ''',
          201,
        ));

        final createdComment = await apiService.createComment(newComment);

        expect(createdComment.id, 1);
        expect(createdComment.content, 'New comment');
      });

      test('should handle comment creation error', () async {
        final newComment = Comment(content: '');

        // Mock error response
        when(mockHttpClient.post(
          Uri.parse('${ApiService.baseUrl}/comments'),
          headers: anyNamed('headers'),
          body: anyNamed('body'),
        )).thenAnswer((_) async => http.Response(
          '{"error": "Content cannot be empty"}',
          400,
        ));

        expect(
          () => apiService.createComment(newComment),
          throwsA(isA<Exception>()),
        );
      });
    });

    group('Users', () {
      test('should fetch user successfully', () async {
        // Mock successful response
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/users/1'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response(
          '''
          {
            "id": 1,
            "username": "testuser",
            "name": "Test User",
            "email": "test@example.com"
          }
          ''',
          200,
        ));

        final user = await apiService.getUser(1);

        expect(user.id, 1);
        expect(user.username, 'testuser');
        expect(user.name, 'Test User');
        expect(user.email, 'test@example.com');
      });

      test('should handle user not found error', () async {
        // Mock error response
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/users/999'),
          headers: anyNamed('headers'),
        )).thenAnswer((_) async => http.Response(
          '{"error": "User not found"}',
          404,
        ));

        expect(
          () => apiService.getUser(999),
          throwsA(isA<Exception>()),
        );
      });
    });

    group('Headers', () {
      test('should use provided headers', () async {
        final customHeaders = {
          'Authorization': 'Bearer custom_token',
          'Content-Type': 'application/json',
        };

        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: customHeaders,
        )).thenAnswer((_) async => http.Response(
          '{"hydra:member": []}',
          200,
        ));

        await apiService.getBlogPosts(headers: customHeaders);

        verify(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: customHeaders,
        )).called(1);
      });

      test('should use default headers when none provided', () async {
        when(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: {'Content-Type': 'application/json'},
        )).thenAnswer((_) async => http.Response(
          '{"hydra:member": []}',
          200,
        ));

        await apiService.getBlogPosts();

        verify(mockHttpClient.get(
          Uri.parse('${ApiService.baseUrl}/blog_posts'),
          headers: {'Content-Type': 'application/json'},
        )).called(1);
      });
    });
  });
}