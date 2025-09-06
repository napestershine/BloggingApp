import 'package:flutter_test/flutter_test.dart';
import 'package:sf5_blog_app/models/user.dart';
import 'package:sf5_blog_app/models/blog_post.dart';
import 'package:sf5_blog_app/models/comment.dart';

void main() {
  group('Model Tests', () {
    test('User model should serialize to/from JSON', () {
      final user = User(
        id: 1,
        username: 'testuser',
        name: 'Test User',
        email: 'test@example.com',
      );

      final json = user.toJson();
      final userFromJson = User.fromJson(json);

      expect(userFromJson.id, equals(user.id));
      expect(userFromJson.username, equals(user.username));
      expect(userFromJson.name, equals(user.name));
      expect(userFromJson.email, equals(user.email));
    });

    test('BlogPost model should serialize to/from JSON', () {
      final blogPost = BlogPost(
        id: 1,
        title: 'Test Blog Post',
        content: 'This is a test blog post content.',
        slug: 'test-blog-post',
      );

      final json = blogPost.toCreateJson();
      
      expect(json['title'], equals(blogPost.title));
      expect(json['content'], equals(blogPost.content));
      expect(json['slug'], equals(blogPost.slug));
    });

    test('Comment model should serialize to/from JSON', () {
      final comment = Comment(
        id: 1,
        content: 'This is a test comment',
      );

      final json = comment.toCreateJson();
      
      expect(json['content'], equals(comment.content));
    });
  });
}