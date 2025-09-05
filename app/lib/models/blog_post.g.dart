// GENERATED CODE - DO NOT MODIFY BY HAND
// This is a minimal stub file for testing without Flutter SDK

part of 'blog_post.dart';

BlogPost _$BlogPostFromJson(Map<String, dynamic> json) => BlogPost(
      id: json['id'] as int?,
      title: json['title'] as String,
      content: json['content'] as String,
      slug: json['slug'] as String?,
      publishedDate: json['published'] == null 
          ? null 
          : DateTime.parse(json['published'] as String),
      author: json['author'] == null
          ? null
          : User.fromJson(json['author'] as Map<String, dynamic>),
      comments: json['comments'] == null
          ? null
          : (json['comments'] as List<dynamic>)
              .map((e) => Comment.fromJson(e as Map<String, dynamic>))
              .toList(),
    );

Map<String, dynamic> _$BlogPostToJson(BlogPost instance) => <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'content': instance.content,
      'slug': instance.slug,
      'published': instance.publishedDate?.toIso8601String(),
      'author': instance.author?.toJson(),
      'comments': instance.comments?.map((e) => e.toJson()).toList(),
    };