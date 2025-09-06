// GENERATED CODE - DO NOT MODIFY BY HAND
// This is a minimal stub file for testing without Flutter SDK

part of 'user.dart';

User _$UserFromJson(Map<String, dynamic> json) => User(
      id: json['id'] as int?,
      username: json['username'] as String,
      name: json['name'] as String,
      email: json['email'] as String?,
    );

Map<String, dynamic> _$UserToJson(User instance) => <String, dynamic>{
      'id': instance.id,
      'username': instance.username,
      'name': instance.name,
      'email': instance.email,
    };