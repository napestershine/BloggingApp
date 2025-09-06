import 'package:json_annotation/json_annotation.dart';
import 'user.dart';

part 'user_follow.g.dart';

@JsonSerializable()
class UserFollowResponse {
  @JsonKey(name: 'following_id')
  final int followingId;
  @JsonKey(name: 'follower_id')
  final int followerId;
  @JsonKey(name: 'is_following')
  final bool isFollowing;
  @JsonKey(name: 'created_at')
  final String? createdAt;

  const UserFollowResponse({
    required this.followingId,
    required this.followerId,
    required this.isFollowing,
    this.createdAt,
  });

  factory UserFollowResponse.fromJson(Map<String, dynamic> json) => 
      _$UserFollowResponseFromJson(json);
  Map<String, dynamic> toJson() => _$UserFollowResponseToJson(this);
}

@JsonSerializable()
class UserFollowStats {
  @JsonKey(name: 'followers_count')
  final int followersCount;
  @JsonKey(name: 'following_count')
  final int followingCount;
  @JsonKey(name: 'is_following')
  final bool? isFollowing;

  const UserFollowStats({
    required this.followersCount,
    required this.followingCount,
    this.isFollowing,
  });

  factory UserFollowStats.fromJson(Map<String, dynamic> json) => 
      _$UserFollowStatsFromJson(json);
  Map<String, dynamic> toJson() => _$UserFollowStatsToJson(this);
}

@JsonSerializable()
class FollowerUser {
  final int id;
  final String username;
  final String name;
  final String? email;

  const FollowerUser({
    required this.id,
    required this.username,
    required this.name,
    this.email,
  });

  factory FollowerUser.fromJson(Map<String, dynamic> json) => 
      _$FollowerUserFromJson(json);
  Map<String, dynamic> toJson() => _$FollowerUserToJson(this);
}