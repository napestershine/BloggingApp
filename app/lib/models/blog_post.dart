import 'package:json_annotation/json_annotation.dart';
import 'user.dart';
import 'comment.dart';

part 'blog_post.g.dart';

@JsonSerializable()
class BlogPost {
  final int? id;
  final String title;
  final String content;
  final String? slug;
  @JsonKey(name: 'published')
  final DateTime? publishedDate;
  final User? author;
  final List<Comment>? comments;

  const BlogPost({
    this.id,
    required this.title,
    required this.content,
    this.slug,
    this.publishedDate,
    this.author,
    this.comments,
  });

  factory BlogPost.fromJson(Map<String, dynamic> json) => _$BlogPostFromJson(json);
  Map<String, dynamic> toJson() => _$BlogPostToJson(this);

  // Helper method to create a new blog post for API submission
  Map<String, dynamic> toCreateJson() {
    return {
      'title': title,
      'content': content,
      'slug': slug,
    };
  }
}