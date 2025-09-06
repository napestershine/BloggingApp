import 'package:flutter/material.dart';
import '../models/notification.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({Key? key}) : super(key: key);

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen>
    with SingleTickerProviderStateMixin {
  final _apiService = ApiService();
  final _authService = AuthService();
  late TabController _tabController;

  List<NotificationModel> _allNotifications = [];
  List<NotificationModel> _unreadNotifications = [];
  bool _isLoading = true;
  WhatsAppSettings? _whatsappSettings;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadNotifications();
    _loadWhatsAppSettings();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadNotifications() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final token = await _authService.getToken();
      final headers = {'Authorization': 'Bearer $token'};
      
      final allNotifications = await _apiService.getNotifications(headers: headers);
      final unreadNotifications = await _apiService.getNotifications(
        isRead: false,
        headers: headers,
      );
      
      setState(() {
        _allNotifications = allNotifications;
        _unreadNotifications = unreadNotifications;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load notifications: $e')),
      );
    }
  }

  Future<void> _loadWhatsAppSettings() async {
    try {
      final token = await _authService.getToken();
      final settings = await _apiService.getWhatsAppSettings(
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        _whatsappSettings = settings;
      });
    } catch (e) {
      print('Error loading WhatsApp settings: $e');
    }
  }

  Future<void> _markAsRead(NotificationModel notification) async {
    if (notification.isRead) return;

    try {
      final token = await _authService.getToken();
      await _apiService.markNotificationAsRead(
        notification.id,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        // Update the notification in both lists
        final allIndex = _allNotifications.indexWhere((n) => n.id == notification.id);
        if (allIndex != -1) {
          _allNotifications[allIndex] = NotificationModel(
            id: notification.id,
            userId: notification.userId,
            type: notification.type,
            message: notification.message,
            isRead: true,
            createdAt: notification.createdAt,
            postId: notification.postId,
            fromUserId: notification.fromUserId,
            fromUserName: notification.fromUserName,
          );
        }
        
        // Remove from unread list
        _unreadNotifications.removeWhere((n) => n.id == notification.id);
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to mark as read: $e')),
      );
    }
  }

  Future<void> _showWhatsAppSettings() async {
    final result = await showDialog<WhatsAppSettings>(
      context: context,
      builder: (context) => WhatsAppSettingsDialog(
        currentSettings: _whatsappSettings,
        apiService: _apiService,
        authService: _authService,
      ),
    );
    
    if (result != null) {
      setState(() {
        _whatsappSettings = result;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications'),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: _showWhatsAppSettings,
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadNotifications,
          ),
        ],
      ),
      body: Column(
        children: [
          // Tabs
          TabBar(
            controller: _tabController,
            tabs: [
              Tab(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('All'),
                    if (_allNotifications.isNotEmpty) ...[
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: Theme.of(context).primaryColor,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          _allNotifications.length.toString(),
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
              ),
              Tab(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Unread'),
                    if (_unreadNotifications.isNotEmpty) ...[
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: Colors.red,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          _unreadNotifications.length.toString(),
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
              ),
              const Tab(text: 'Settings'),
            ],
          ),
          
          // Tab content
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : TabBarView(
                    controller: _tabController,
                    children: [
                      // All notifications
                      _buildNotificationsList(_allNotifications, 'No notifications yet'),
                      
                      // Unread notifications
                      _buildNotificationsList(_unreadNotifications, 'No unread notifications'),
                      
                      // Settings
                      _buildSettingsTab(),
                    ],
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildNotificationsList(List<NotificationModel> notifications, String emptyMessage) {
    if (notifications.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.notifications_none,
              size: 64,
              color: Colors.grey[400],
            ),
            const SizedBox(height: 16),
            Text(
              emptyMessage,
              style: TextStyle(
                fontSize: 18,
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _loadNotifications,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: notifications.length,
        itemBuilder: (context, index) {
          final notification = notifications[index];
          return Card(
            child: ListTile(
              leading: _buildNotificationIcon(notification.type),
              title: Text(notification.message),
              subtitle: Text(
                _formatDateTime(notification.createdAt),
                style: TextStyle(
                  color: Colors.grey[600],
                  fontSize: 12,
                ),
              ),
              trailing: notification.isRead
                  ? null
                  : Container(
                      width: 8,
                      height: 8,
                      decoration: const BoxDecoration(
                        color: Colors.red,
                        shape: BoxShape.circle,
                      ),
                    ),
              onTap: () => _markAsRead(notification),
            ),
          );
        },
      ),
    );
  }

  Widget _buildSettingsTab() {
    if (_whatsappSettings == null) {
      return const Center(child: CircularProgressIndicator());
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'WhatsApp Notifications',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  
                  if (_whatsappSettings!.whatsappNumber != null) ...[
                    Text('Phone Number: ${_whatsappSettings!.whatsappNumber}'),
                    const SizedBox(height: 8),
                  ],
                  
                  Text(
                    'Status: ${_whatsappSettings!.whatsappNotificationsEnabled ? "Enabled" : "Disabled"}',
                    style: TextStyle(
                      color: _whatsappSettings!.whatsappNotificationsEnabled
                          ? Colors.green
                          : Colors.red,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  
                  const Text('Notification Types:'),
                  CheckboxListTile(
                    title: const Text('New Posts'),
                    value: _whatsappSettings!.notifyOnNewPosts,
                    onChanged: null, // Read-only display
                  ),
                  CheckboxListTile(
                    title: const Text('Comments'),
                    value: _whatsappSettings!.notifyOnComments,
                    onChanged: null, // Read-only display
                  ),
                  CheckboxListTile(
                    title: const Text('Mentions'),
                    value: _whatsappSettings!.notifyOnMentions,
                    onChanged: null, // Read-only display
                  ),
                  const SizedBox(height: 16),
                  
                  ElevatedButton(
                    onPressed: _showWhatsAppSettings,
                    child: const Text('Update Settings'),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNotificationIcon(String type) {
    IconData iconData;
    Color color;
    
    switch (type) {
      case 'follow':
        iconData = Icons.person_add;
        color = Colors.blue;
        break;
      case 'post_like':
        iconData = Icons.favorite;
        color = Colors.red;
        break;
      case 'post_comment':
        iconData = Icons.comment;
        color = Colors.green;
        break;
      case 'mention':
        iconData = Icons.alternate_email;
        color = Colors.orange;
        break;
      default:
        iconData = Icons.notifications;
        color = Colors.grey;
    }
    
    return CircleAvatar(
      backgroundColor: color.withOpacity(0.2),
      child: Icon(iconData, color: color),
    );
  }

  String _formatDateTime(String dateTimeStr) {
    try {
      final dateTime = DateTime.parse(dateTimeStr);
      final now = DateTime.now();
      final difference = now.difference(dateTime);
      
      if (difference.inDays > 0) {
        return '${difference.inDays}d ago';
      } else if (difference.inHours > 0) {
        return '${difference.inHours}h ago';
      } else if (difference.inMinutes > 0) {
        return '${difference.inMinutes}m ago';
      } else {
        return 'Just now';
      }
    } catch (e) {
      return dateTimeStr;
    }
  }
}

class WhatsAppSettingsDialog extends StatefulWidget {
  final WhatsAppSettings? currentSettings;
  final ApiService apiService;
  final AuthService authService;

  const WhatsAppSettingsDialog({
    Key? key,
    required this.currentSettings,
    required this.apiService,
    required this.authService,
  }) : super(key: key);

  @override
  State<WhatsAppSettingsDialog> createState() => _WhatsAppSettingsDialogState();
}

class _WhatsAppSettingsDialogState extends State<WhatsAppSettingsDialog> {
  final _phoneController = TextEditingController();
  bool _notificationsEnabled = false;
  bool _notifyOnNewPosts = true;
  bool _notifyOnComments = true;
  bool _notifyOnMentions = true;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    if (widget.currentSettings != null) {
      _phoneController.text = widget.currentSettings!.whatsappNumber ?? '';
      _notificationsEnabled = widget.currentSettings!.whatsappNotificationsEnabled;
      _notifyOnNewPosts = widget.currentSettings!.notifyOnNewPosts;
      _notifyOnComments = widget.currentSettings!.notifyOnComments;
      _notifyOnMentions = widget.currentSettings!.notifyOnMentions;
    }
  }

  @override
  void dispose() {
    _phoneController.dispose();
    super.dispose();
  }

  Future<void> _saveSettings() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final token = await widget.authService.getToken();
      final update = WhatsAppSettingsUpdate(
        whatsappNumber: _phoneController.text.trim().isEmpty ? null : _phoneController.text.trim(),
        whatsappNotificationsEnabled: _notificationsEnabled,
        notifyOnNewPosts: _notifyOnNewPosts,
        notifyOnComments: _notifyOnComments,
        notifyOnMentions: _notifyOnMentions,
      );
      
      final result = await widget.apiService.updateWhatsAppSettings(
        update,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      Navigator.of(context).pop(result);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to update settings: $e')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('WhatsApp Settings'),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: _phoneController,
              decoration: const InputDecoration(
                labelText: 'Phone Number',
                hintText: '+1234567890',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.phone,
            ),
            const SizedBox(height: 16),
            
            SwitchListTile(
              title: const Text('Enable WhatsApp Notifications'),
              value: _notificationsEnabled,
              onChanged: (value) {
                setState(() {
                  _notificationsEnabled = value;
                });
              },
            ),
            
            if (_notificationsEnabled) ...[
              SwitchListTile(
                title: const Text('New Posts'),
                value: _notifyOnNewPosts,
                onChanged: (value) {
                  setState(() {
                    _notifyOnNewPosts = value;
                  });
                },
              ),
              SwitchListTile(
                title: const Text('Comments'),
                value: _notifyOnComments,
                onChanged: (value) {
                  setState(() {
                    _notifyOnComments = value;
                  });
                },
              ),
              SwitchListTile(
                title: const Text('Mentions'),
                value: _notifyOnMentions,
                onChanged: (value) {
                  setState(() {
                    _notifyOnMentions = value;
                  });
                },
              ),
            ],
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _isLoading ? null : _saveSettings,
          child: _isLoading
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Text('Save'),
        ),
      ],
    );
  }
}