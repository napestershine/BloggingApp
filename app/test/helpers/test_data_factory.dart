import 'package:sf5_blog_app/models/blog_post.dart';
import 'package:sf5_blog_app/models/comment.dart';
import 'package:sf5_blog_app/models/user.dart';

/// Factory class for creating test data objects with consistent and realistic data
class TestDataFactory {
  static int _userIdCounter = 1;
  static int _blogPostIdCounter = 1;
  static int _commentIdCounter = 1;

  /// Creates a test user with default or custom values
  static User createUser({
    int? id,
    String? username,
    String? name,
    String? email,
  }) {
    final userId = id ?? _userIdCounter++;
    return User(
      id: userId,
      username: username ?? 'user$userId',
      name: name ?? 'Test User $userId',
      email: email ?? 'user$userId@example.com',
    );
  }

  /// Creates multiple test users
  static List<User> createUsers(int count) {
    return List.generate(count, (index) => createUser());
  }

  /// Creates a test blog post with default or custom values
  static BlogPost createBlogPost({
    int? id,
    String? title,
    String? content,
    String? slug,
    DateTime? publishedDate,
    User? author,
    List<Comment>? comments,
  }) {
    final postId = id ?? _blogPostIdCounter++;
    return BlogPost(
      id: postId,
      title: title ?? 'Test Blog Post $postId',
      content: content ?? 'This is the content for test blog post $postId. It contains some sample text to test the display and functionality.',
      slug: slug ?? 'test-blog-post-$postId',
      publishedDate: publishedDate ?? DateTime.now().subtract(Duration(hours: postId)),
      author: author ?? createUser(),
      comments: comments,
    );
  }

  /// Creates multiple test blog posts
  static List<BlogPost> createBlogPosts(int count, {User? author}) {
    return List.generate(count, (index) => createBlogPost(
      author: author ?? createUser(),
    ));
  }

  /// Creates a test blog post with comments
  static BlogPost createBlogPostWithComments({
    int commentCount = 3,
    User? author,
  }) {
    final post = createBlogPost(author: author);
    final comments = createComments(commentCount, blogPost: post);
    
    return BlogPost(
      id: post.id,
      title: post.title,
      content: post.content,
      slug: post.slug,
      publishedDate: post.publishedDate,
      author: post.author,
      comments: comments,
    );
  }

  /// Creates a test comment with default or custom values
  static Comment createComment({
    int? id,
    String? content,
    DateTime? publishedDate,
    User? author,
    BlogPost? blogPost,
  }) {
    final commentId = id ?? _commentIdCounter++;
    return Comment(
      id: commentId,
      content: content ?? 'This is test comment $commentId with some sample content.',
      publishedDate: publishedDate ?? DateTime.now().subtract(Duration(minutes: commentId * 15)),
      author: author ?? createUser(),
      blogPost: blogPost,
    );
  }

  /// Creates multiple test comments
  static List<Comment> createComments(int count, {User? author, BlogPost? blogPost}) {
    return List.generate(count, (index) => createComment(
      author: author ?? createUser(),
      blogPost: blogPost,
    ));
  }

  /// Creates a comment with specific time ago
  static Comment createCommentWithTimeAgo({
    Duration? timeAgo,
    String? content,
    User? author,
  }) {
    return createComment(
      content: content,
      publishedDate: DateTime.now().subtract(timeAgo ?? const Duration(hours: 1)),
      author: author,
    );
  }

  /// Creates a blog post for specific test scenarios
  static BlogPost createLongBlogPost() {
    return createBlogPost(
      title: 'This is a very long blog post title that should test text truncation and wrapping behavior in the UI components',
      content: '''This is a very long blog post content that spans multiple lines and contains various types of content. 

It includes multiple paragraphs to test how the UI handles longer text content. This paragraph contains enough text to test text overflow and truncation behavior.

The content also includes some special characters and formatting that might be encountered in real blog posts. This helps ensure that the UI components can handle various types of content gracefully.

This long content is particularly useful for testing scrolling behavior, text rendering performance, and layout constraints in different screen sizes.''',
    );
  }

  /// Creates an empty blog post for testing empty states
  static BlogPost createMinimalBlogPost() {
    return BlogPost(
      title: 'Minimal Post',
      content: 'Short content.',
    );
  }

  /// Creates blog post data for pagination testing
  static List<BlogPost> createPaginatedBlogPosts({
    int page = 1,
    int pageSize = 10,
    User? author,
  }) {
    final startIndex = (page - 1) * pageSize;
    return List.generate(pageSize, (index) {
      final postNumber = startIndex + index + 1;
      return createBlogPost(
        title: 'Blog Post Page $page Item $postNumber',
        author: author ?? createUser(),
      );
    });
  }

  /// Creates test data for error scenarios
  static BlogPost createBlogPostWithErrors() {
    return BlogPost(
      id: -1,
      title: '',
      content: '',
      slug: null,
      publishedDate: null,
      author: null,
      comments: null,
    );
  }

  /// Creates test authentication data
  static Map<String, dynamic> createLoginResponse({
    String? token,
    User? user,
  }) {
    return {
      'token': token ?? 'test_jwt_token_${DateTime.now().millisecondsSinceEpoch}',
      'user': user?.toJson() ?? createUser().toJson(),
    };
  }

  /// Creates test API error response
  static Map<String, dynamic> createErrorResponse({
    String? message,
    int? statusCode,
  }) {
    return {
      'error': message ?? 'Test error message',
      'status_code': statusCode ?? 400,
      'timestamp': DateTime.now().toIso8601String(),
    };
  }

  /// Creates test data for search/filter scenarios
  static List<BlogPost> createSearchableBlogPosts() {
    return [
      createBlogPost(title: 'Flutter Development Tips', content: 'Learn about Flutter widgets and state management.'),
      createBlogPost(title: 'Dart Programming Guide', content: 'Master Dart language features and best practices.'),
      createBlogPost(title: 'Mobile App Testing', content: 'Comprehensive guide to testing Flutter applications.'),
      createBlogPost(title: 'UI/UX Design Principles', content: 'Design beautiful and user-friendly mobile interfaces.'),
      createBlogPost(title: 'API Integration Patterns', content: 'Best practices for integrating REST APIs in Flutter.'),
    ];
  }

  /// Resets all counters (useful for test isolation)
  static void resetCounters() {
    _userIdCounter = 1;
    _blogPostIdCounter = 1;
    _commentIdCounter = 1;
  }

  /// Creates test data for performance testing
  static List<BlogPost> createLargeDataset(int count) {
    resetCounters();
    return List.generate(count, (index) {
      return createBlogPost(
        title: 'Performance Test Post ${index + 1}',
        content: 'Content for performance testing post ${index + 1}. ' * 10,
      );
    });
  }

  /// Creates test data with specific date ranges
  static List<BlogPost> createBlogPostsWithDateRange({
    required DateTime startDate,
    required DateTime endDate,
    int count = 10,
  }) {
    final daysDifference = endDate.difference(startDate).inDays;
    return List.generate(count, (index) {
      final publishedDate = startDate.add(Duration(
        days: (daysDifference * index / count).round(),
      ));
      return createBlogPost(publishedDate: publishedDate);
    });
  }
}