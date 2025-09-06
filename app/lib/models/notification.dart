import 'package:json_annotation/json_annotation.dart';

part 'notification.g.dart';

@JsonSerializable()
class NotificationModel {
  final int id;
  @JsonKey(name: 'user_id')
  final int userId;
  final String type;
  final String message;
  @JsonKey(name: 'is_read')
  final bool isRead;
  @JsonKey(name: 'created_at')
  final String createdAt;
  @JsonKey(name: 'post_id')
  final int? postId;
  @JsonKey(name: 'from_user_id')
  final int? fromUserId;
  @JsonKey(name: 'from_user_name')
  final String? fromUserName;

  const NotificationModel({
    required this.id,
    required this.userId,
    required this.type,
    required this.message,
    required this.isRead,
    required this.createdAt,
    this.postId,
    this.fromUserId,
    this.fromUserName,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json) => 
      _$NotificationModelFromJson(json);
  Map<String, dynamic> toJson() => _$NotificationModelToJson(this);
}

@JsonSerializable()
class WhatsAppSettings {
  @JsonKey(name: 'whatsapp_number')
  final String? whatsappNumber;
  @JsonKey(name: 'whatsapp_notifications_enabled')
  final bool whatsappNotificationsEnabled;
  @JsonKey(name: 'notify_on_new_posts')
  final bool notifyOnNewPosts;
  @JsonKey(name: 'notify_on_comments')
  final bool notifyOnComments;
  @JsonKey(name: 'notify_on_mentions')
  final bool notifyOnMentions;

  const WhatsAppSettings({
    this.whatsappNumber,
    required this.whatsappNotificationsEnabled,
    required this.notifyOnNewPosts,
    required this.notifyOnComments,
    required this.notifyOnMentions,
  });

  factory WhatsAppSettings.fromJson(Map<String, dynamic> json) => 
      _$WhatsAppSettingsFromJson(json);
  Map<String, dynamic> toJson() => _$WhatsAppSettingsToJson(this);
}

@JsonSerializable()
class WhatsAppSettingsUpdate {
  @JsonKey(name: 'whatsapp_number')
  final String? whatsappNumber;
  @JsonKey(name: 'whatsapp_notifications_enabled')
  final bool? whatsappNotificationsEnabled;
  @JsonKey(name: 'notify_on_new_posts')
  final bool? notifyOnNewPosts;
  @JsonKey(name: 'notify_on_comments')
  final bool? notifyOnComments;
  @JsonKey(name: 'notify_on_mentions')
  final bool? notifyOnMentions;

  const WhatsAppSettingsUpdate({
    this.whatsappNumber,
    this.whatsappNotificationsEnabled,
    this.notifyOnNewPosts,
    this.notifyOnComments,
    this.notifyOnMentions,
  });

  factory WhatsAppSettingsUpdate.fromJson(Map<String, dynamic> json) => 
      _$WhatsAppSettingsUpdateFromJson(json);
  Map<String, dynamic> toJson() => _$WhatsAppSettingsUpdateToJson(this);
}