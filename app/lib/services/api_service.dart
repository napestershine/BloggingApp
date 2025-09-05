import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/blog_post.dart';
import '../models/comment.dart';
import '../models/user.dart';

class ApiService {
  // Update this URL to match your Symfony API endpoint
  static const String baseUrl = 'http://localhost:8080/api';

  // Blog Posts
  Future<List<BlogPost>> getBlogPosts({Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/blog_posts'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> blogPostsJson = data['hydra:member'] ?? data;
        
        return blogPostsJson
            .map((json) => BlogPost.fromJson(json))
            .toList();
      } else {
        throw Exception('Failed to load blog posts: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching blog posts: $e');
      throw Exception('Failed to load blog posts');
    }
  }

  Future<BlogPost> getBlogPost(int id, {Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/blog_posts/$id'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return BlogPost.fromJson(data);
      } else {
        throw Exception('Failed to load blog post: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching blog post: $e');
      throw Exception('Failed to load blog post');
    }
  }

  Future<BlogPost> createBlogPost(BlogPost blogPost, {Map<String, String>? headers}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/blog_posts'),
        headers: headers ?? {'Content-Type': 'application/json'},
        body: json.encode(blogPost.toCreateJson()),
      );

      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        return BlogPost.fromJson(data);
      } else {
        throw Exception('Failed to create blog post: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('Error creating blog post: $e');
      throw Exception('Failed to create blog post');
    }
  }

  Future<BlogPost> updateBlogPost(int id, BlogPost blogPost, {Map<String, String>? headers}) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/blog_posts/$id'),
        headers: headers ?? {'Content-Type': 'application/json'},
        body: json.encode(blogPost.toCreateJson()),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return BlogPost.fromJson(data);
      } else {
        throw Exception('Failed to update blog post: ${response.statusCode}');
      }
    } catch (e) {
      print('Error updating blog post: $e');
      throw Exception('Failed to update blog post');
    }
  }

  Future<void> deleteBlogPost(int id, {Map<String, String>? headers}) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/blog_posts/$id'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode != 204) {
        throw Exception('Failed to delete blog post: ${response.statusCode}');
      }
    } catch (e) {
      print('Error deleting blog post: $e');
      throw Exception('Failed to delete blog post');
    }
  }

  // Comments
  Future<List<Comment>> getComments({Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/comments'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> commentsJson = data['hydra:member'] ?? data;
        
        return commentsJson
            .map((json) => Comment.fromJson(json))
            .toList();
      } else {
        throw Exception('Failed to load comments: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching comments: $e');
      throw Exception('Failed to load comments');
    }
  }

  Future<List<Comment>> getBlogPostComments(int blogPostId, {Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/blog_posts/$blogPostId/comments'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> commentsJson = data['hydra:member'] ?? data;
        
        return commentsJson
            .map((json) => Comment.fromJson(json))
            .toList();
      } else {
        throw Exception('Failed to load comments: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching comments: $e');
      throw Exception('Failed to load comments');
    }
  }

  Future<Comment> createComment(Comment comment, {Map<String, String>? headers}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/comments'),
        headers: headers ?? {'Content-Type': 'application/json'},
        body: json.encode(comment.toCreateJson()),
      );

      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        return Comment.fromJson(data);
      } else {
        throw Exception('Failed to create comment: ${response.statusCode}');
      }
    } catch (e) {
      print('Error creating comment: $e');
      throw Exception('Failed to create comment');
    }
  }

  // Users
  Future<User> getUser(int id, {Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/users/$id'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return User.fromJson(data);
      } else {
        throw Exception('Failed to load user: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching user: $e');
      throw Exception('Failed to load user');
    }
  }
}