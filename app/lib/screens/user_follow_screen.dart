import 'package:flutter/material.dart';
import '../models/user_follow.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';

class UserFollowScreen extends StatefulWidget {
  final int userId;
  final String username;

  const UserFollowScreen({
    Key? key,
    required this.userId,
    required this.username,
  }) : super(key: key);

  @override
  State<UserFollowScreen> createState() => _UserFollowScreenState();
}

class _UserFollowScreenState extends State<UserFollowScreen>
    with SingleTickerProviderStateMixin {
  final _apiService = ApiService();
  final _authService = AuthService();
  late TabController _tabController;

  UserFollowStats? _stats;
  List<FollowerUser> _followers = [];
  List<FollowerUser> _following = [];
  bool _isLoading = true;
  bool _isLoadingFollowers = false;
  bool _isLoadingFollowing = false;
  bool _isFollowActionLoading = false;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _loadStats();
    _loadFollowers();
    _loadFollowing();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadStats() async {
    try {
      final token = await _authService.getToken();
      final stats = await _apiService.getUserFollowStats(
        widget.userId,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        _stats = stats;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load user stats: $e')),
      );
    }
  }

  Future<void> _loadFollowers() async {
    setState(() {
      _isLoadingFollowers = true;
    });

    try {
      final token = await _authService.getToken();
      final followers = await _apiService.getUserFollowers(
        widget.userId,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        _followers = followers;
        _isLoadingFollowers = false;
      });
    } catch (e) {
      setState(() {
        _isLoadingFollowers = false;
      });
      print('Error loading followers: $e');
    }
  }

  Future<void> _loadFollowing() async {
    setState(() {
      _isLoadingFollowing = true;
    });

    try {
      final token = await _authService.getToken();
      final following = await _apiService.getUserFollowing(
        widget.userId,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        _following = following;
        _isLoadingFollowing = false;
      });
    } catch (e) {
      setState(() {
        _isLoadingFollowing = false;
      });
      print('Error loading following: $e');
    }
  }

  Future<void> _toggleFollow() async {
    if (_stats == null || _isFollowActionLoading) return;

    setState(() {
      _isFollowActionLoading = true;
    });

    try {
      final token = await _authService.getToken();
      
      if (_stats!.isFollowing == true) {
        await _apiService.unfollowUser(
          widget.userId,
          headers: {'Authorization': 'Bearer $token'},
        );
      } else {
        await _apiService.followUser(
          widget.userId,
          headers: {'Authorization': 'Bearer $token'},
        );
      }
      
      // Reload stats to get updated counts
      await _loadStats();
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            _stats!.isFollowing == true
                ? 'Following ${widget.username}'
                : 'Unfollowed ${widget.username}',
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to update follow status: $e')),
      );
    } finally {
      setState(() {
        _isFollowActionLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.username}\'s Network'),
        elevation: 0,
        actions: [
          if (_stats != null && _stats!.isFollowing != null)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: _isFollowActionLoading
                  ? const Center(
                      child: SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      ),
                    )
                  : ElevatedButton.icon(
                      icon: Icon(
                        _stats!.isFollowing == true
                            ? Icons.person_remove
                            : Icons.person_add,
                      ),
                      label: Text(
                        _stats!.isFollowing == true ? 'Unfollow' : 'Follow',
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: _stats!.isFollowing == true
                            ? Colors.grey
                            : Theme.of(context).primaryColor,
                      ),
                      onPressed: _toggleFollow,
                    ),
            ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                // Stats header
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Theme.of(context).cardColor,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.1),
                        blurRadius: 4,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildStatColumn(
                        'Followers',
                        _stats?.followersCount.toString() ?? '0',
                      ),
                      _buildStatColumn(
                        'Following',
                        _stats?.followingCount.toString() ?? '0',
                      ),
                    ],
                  ),
                ),
                
                // Tabs
                TabBar(
                  controller: _tabController,
                  tabs: const [
                    Tab(text: 'Followers'),
                    Tab(text: 'Following'),
                  ],
                ),
                
                // Tab content
                Expanded(
                  child: TabBarView(
                    controller: _tabController,
                    children: [
                      // Followers tab
                      _buildUserList(
                        users: _followers,
                        isLoading: _isLoadingFollowers,
                        emptyMessage: 'No followers yet',
                        onRefresh: _loadFollowers,
                      ),
                      
                      // Following tab
                      _buildUserList(
                        users: _following,
                        isLoading: _isLoadingFollowing,
                        emptyMessage: 'Not following anyone yet',
                        onRefresh: _loadFollowing,
                      ),
                    ],
                  ),
                ),
              ],
            ),
    );
  }

  Widget _buildStatColumn(String label, String count) {
    return Column(
      children: [
        Text(
          count,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 16,
            color: Colors.grey[600],
          ),
        ),
      ],
    );
  }

  Widget _buildUserList({
    required List<FollowerUser> users,
    required bool isLoading,
    required String emptyMessage,
    required VoidCallback onRefresh,
  }) {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (users.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.people_outline,
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
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: onRefresh,
              child: const Text('Refresh'),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: () async => onRefresh(),
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: users.length,
        itemBuilder: (context, index) {
          final user = users[index];
          return Card(
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: Theme.of(context).primaryColor,
                child: Text(
                  user.username.substring(0, 1).toUpperCase(),
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              title: Text(user.name),
              subtitle: Text('@${user.username}'),
              trailing: const Icon(Icons.arrow_forward_ios),
              onTap: () {
                // Navigate to user profile
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(
                    builder: (context) => UserFollowScreen(
                      userId: user.id,
                      username: user.username,
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}