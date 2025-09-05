import 'package:json_annotation/json_annotation.dart';
import 'user.dart';
import 'blog_post.dart';

part 'comment.g.dart';

@JsonSerializable()
class Comment {
  final int? id;
  final String content;
  @JsonKey(name: 'published')
  final DateTime? publishedDate;
  final User? author;
  @JsonKey(name: 'blogPost')
  final BlogPost? blogPost;

  const Comment({
    this.id,
    required this.content,
    this.publishedDate,
    this.author,
    this.blogPost,
  });

  factory Comment.fromJson(Map<String, dynamic> json) => _$CommentFromJson(json);
  Map<String, dynamic> toJson() => _$CommentToJson(this);

  // Helper method to create a new comment for API submission
  Map<String, dynamic> toCreateJson() {
    return {
      'content': content,
    };
  }
}