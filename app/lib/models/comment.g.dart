// GENERATED CODE - DO NOT MODIFY BY HAND
// This is a minimal stub file for testing without Flutter SDK

part of 'comment.dart';

Comment _$CommentFromJson(Map<String, dynamic> json) => Comment(
      id: json['id'] as int?,
      content: json['content'] as String,
      publishedDate: json['published'] == null 
          ? null 
          : DateTime.parse(json['published'] as String),
      author: json['author'] == null
          ? null
          : User.fromJson(json['author'] as Map<String, dynamic>),
      blogPost: json['blogPost'] == null
          ? null
          : BlogPost.fromJson(json['blogPost'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$CommentToJson(Comment instance) => <String, dynamic>{
      'id': instance.id,
      'content': instance.content,
      'published': instance.publishedDate?.toIso8601String(),
      'author': instance.author?.toJson(),
      'blogPost': instance.blogPost?.toJson(),
    };