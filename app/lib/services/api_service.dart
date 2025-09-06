import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/blog_post.dart';
import '../models/comment.dart';
import '../models/user.dart';
import '../models/search_result.dart';
import '../models/user_follow.dart';
import '../models/notification.dart';
import '../models/bookmark.dart';

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

  // Search API
  Future<List<BlogPost>> searchPosts({
    required String query,
    String? category,
    String? tag,
    String? author,
    int skip = 0,
    int limit = 20,
    Map<String, String>? headers,
  }) async {
    try {
      final queryParams = {
        'q': query,
        'skip': skip.toString(),
        'limit': limit.toString(),
      };
      
      if (category != null) queryParams['category'] = category;
      if (tag != null) queryParams['tag'] = tag;
      if (author != null) queryParams['author'] = author;
      
      final uri = Uri.parse('$baseUrl/search/').replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => BlogPost.fromJson(json)).toList();
      } else {
        throw Exception('Failed to search posts: ${response.statusCode}');
      }
    } catch (e) {
      print('Error searching posts: $e');
      throw Exception('Failed to search posts');
    }
  }

  Future<List<SearchSuggestion>> getSearchSuggestions({
    required String query,
    int limit = 5,
    Map<String, String>? headers,
  }) async {
    try {
      final queryParams = {
        'q': query,
        'limit': limit.toString(),
      };
      
      final uri = Uri.parse('$baseUrl/search/suggestions').replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => SearchSuggestion.fromJson(json)).toList();
      } else {
        throw Exception('Failed to get search suggestions: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting search suggestions: $e');
      throw Exception('Failed to get search suggestions');
    }
  }

  Future<SearchFilters> getSearchFilters({Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/search/filters'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return SearchFilters.fromJson(data);
      } else {
        throw Exception('Failed to get search filters: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting search filters: $e');
      throw Exception('Failed to get search filters');
    }
  }

  // User Follow API
  Future<UserFollowResponse> followUser(int userId, {Map<String, String>? headers}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/follow/users/$userId'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        return UserFollowResponse.fromJson(data);
      } else {
        throw Exception('Failed to follow user: ${response.statusCode}');
      }
    } catch (e) {
      print('Error following user: $e');
      throw Exception('Failed to follow user');
    }
  }

  Future<UserFollowResponse> unfollowUser(int userId, {Map<String, String>? headers}) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/follow/users/$userId'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return UserFollowResponse.fromJson(data);
      } else {
        throw Exception('Failed to unfollow user: ${response.statusCode}');
      }
    } catch (e) {
      print('Error unfollowing user: $e');
      throw Exception('Failed to unfollow user');
    }
  }

  Future<List<FollowerUser>> getUserFollowers(int userId, {
    int skip = 0,
    int limit = 20,
    Map<String, String>? headers,
  }) async {
    try {
      final queryParams = {
        'skip': skip.toString(),
        'limit': limit.toString(),
      };
      
      final uri = Uri.parse('$baseUrl/follow/users/$userId/followers').replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => FollowerUser.fromJson(json)).toList();
      } else {
        throw Exception('Failed to get followers: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting followers: $e');
      throw Exception('Failed to get followers');
    }
  }

  Future<List<FollowerUser>> getUserFollowing(int userId, {
    int skip = 0,
    int limit = 20,
    Map<String, String>? headers,
  }) async {
    try {
      final queryParams = {
        'skip': skip.toString(),
        'limit': limit.toString(),
      };
      
      final uri = Uri.parse('$baseUrl/follow/users/$userId/following').replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => FollowerUser.fromJson(json)).toList();
      } else {
        throw Exception('Failed to get following: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting following: $e');
      throw Exception('Failed to get following');
    }
  }

  Future<UserFollowStats> getUserFollowStats(int userId, {Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/follow/users/$userId/stats'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return UserFollowStats.fromJson(data);
      } else {
        throw Exception('Failed to get follow stats: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting follow stats: $e');
      throw Exception('Failed to get follow stats');
    }
  }

  // Notifications API
  Future<List<NotificationModel>> getNotifications({
    bool? isRead,
    int skip = 0,
    int limit = 20,
    Map<String, String>? headers,
  }) async {
    try {
      final queryParams = {
        'skip': skip.toString(),
        'limit': limit.toString(),
      };
      
      if (isRead != null) queryParams['is_read'] = isRead.toString();
      
      final uri = Uri.parse('$baseUrl/notifications/').replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => NotificationModel.fromJson(json)).toList();
      } else {
        throw Exception('Failed to get notifications: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting notifications: $e');
      throw Exception('Failed to get notifications');
    }
  }

  Future<void> markNotificationAsRead(int notificationId, {Map<String, String>? headers}) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/notifications/$notificationId/read'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to mark notification as read: ${response.statusCode}');
      }
    } catch (e) {
      print('Error marking notification as read: $e');
      throw Exception('Failed to mark notification as read');
    }
  }

  Future<WhatsAppSettings> getWhatsAppSettings({Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/notifications/whatsapp'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return WhatsAppSettings.fromJson(data);
      } else {
        throw Exception('Failed to get WhatsApp settings: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting WhatsApp settings: $e');
      throw Exception('Failed to get WhatsApp settings');
    }
  }

  Future<WhatsAppSettings> updateWhatsAppSettings(
    WhatsAppSettingsUpdate settings, 
    {Map<String, String>? headers}
  ) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/notifications/whatsapp'),
        headers: headers ?? {'Content-Type': 'application/json'},
        body: json.encode(settings.toJson()),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return WhatsAppSettings.fromJson(data);
      } else {
        throw Exception('Failed to update WhatsApp settings: ${response.statusCode}');
      }
    } catch (e) {
      print('Error updating WhatsApp settings: $e');
      throw Exception('Failed to update WhatsApp settings');
    }
  }

  // Bookmarks API
  Future<BookmarkResponse> bookmarkPost(int postId, {Map<String, String>? headers}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/bookmarks/posts/$postId'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        return BookmarkResponse.fromJson(data);
      } else {
        throw Exception('Failed to bookmark post: ${response.statusCode}');
      }
    } catch (e) {
      print('Error bookmarking post: $e');
      throw Exception('Failed to bookmark post');
    }
  }

  Future<void> removeBookmark(int postId, {Map<String, String>? headers}) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/bookmarks/posts/$postId'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to remove bookmark: ${response.statusCode}');
      }
    } catch (e) {
      print('Error removing bookmark: $e');
      throw Exception('Failed to remove bookmark');
    }
  }

  Future<List<BlogPost>> getUserBookmarks({
    int skip = 0,
    int limit = 20,
    Map<String, String>? headers,
  }) async {
    try {
      final queryParams = {
        'skip': skip.toString(),
        'limit': limit.toString(),
      };
      
      final uri = Uri.parse('$baseUrl/bookmarks/').replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => BlogPost.fromJson(json)).toList();
      } else {
        throw Exception('Failed to get bookmarks: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting bookmarks: $e');
      throw Exception('Failed to get bookmarks');
    }
  }

  Future<BookmarkStats> getPostBookmarkStats(int postId, {Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/bookmarks/posts/$postId'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return BookmarkStats.fromJson(data);
      } else {
        throw Exception('Failed to get bookmark stats: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting bookmark stats: $e');
      throw Exception('Failed to get bookmark stats');
    }
  }

  Future<BookmarkStats> getUserBookmarkStats({Map<String, String>? headers}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/bookmarks/stats'),
        headers: headers ?? {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return BookmarkStats.fromJson(data);
      } else {
        throw Exception('Failed to get user bookmark stats: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting user bookmark stats: $e');
      throw Exception('Failed to get user bookmark stats');
    }
  }
}