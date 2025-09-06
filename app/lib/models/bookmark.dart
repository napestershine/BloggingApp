import 'package:json_annotation/json_annotation.dart';
import 'blog_post.dart';

part 'bookmark.g.dart';

@JsonSerializable()
class BookmarkResponse {
  final int id;
  @JsonKey(name: 'user_id')
  final int userId;
  @JsonKey(name: 'post_id')
  final int postId;
  @JsonKey(name: 'created_at')
  final String createdAt;
  final BookmarkPost? post;

  const BookmarkResponse({
    required this.id,
    required this.userId,
    required this.postId,
    required this.createdAt,
    this.post,
  });

  factory BookmarkResponse.fromJson(Map<String, dynamic> json) => 
      _$BookmarkResponseFromJson(json);
  Map<String, dynamic> toJson() => _$BookmarkResponseToJson(this);
}

@JsonSerializable()
class BookmarkPost {
  final int id;
  final String title;
  final String slug;
  final String author;

  const BookmarkPost({
    required this.id,
    required this.title,
    required this.slug,
    required this.author,
  });

  factory BookmarkPost.fromJson(Map<String, dynamic> json) => 
      _$BookmarkPostFromJson(json);
  Map<String, dynamic> toJson() => _$BookmarkPostToJson(this);
}

@JsonSerializable()
class BookmarkStats {
  @JsonKey(name: 'total_bookmarks')
  final int totalBookmarks;
  @JsonKey(name: 'is_bookmarked')
  final bool? isBookmarked;

  const BookmarkStats({
    required this.totalBookmarks,
    this.isBookmarked,
  });

  factory BookmarkStats.fromJson(Map<String, dynamic> json) => 
      _$BookmarkStatsFromJson(json);
  Map<String, dynamic> toJson() => _$BookmarkStatsToJson(this);
}