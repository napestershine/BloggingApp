import 'package:flutter/material.dart';
import '../models/blog_post.dart';
import '../models/bookmark.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../widgets/blog_post_card.dart';

class BookmarksScreen extends StatefulWidget {
  const BookmarksScreen({Key? key}) : super(key: key);

  @override
  State<BookmarksScreen> createState() => _BookmarksScreenState();
}

class _BookmarksScreenState extends State<BookmarksScreen> {
  final _apiService = ApiService();
  final _authService = AuthService();

  List<BlogPost> _bookmarkedPosts = [];
  BookmarkStats? _stats;
  bool _isLoading = true;
  bool _isLoadingMore = false;
  int _currentPage = 0;
  final int _pageSize = 20;

  @override
  void initState() {
    super.initState();
    _loadBookmarks();
    _loadStats();
  }

  Future<void> _loadBookmarks({bool loadMore = false}) async {
    if (loadMore) {
      setState(() {
        _isLoadingMore = true;
      });
    } else {
      setState(() {
        _isLoading = true;
        _currentPage = 0;
        _bookmarkedPosts = [];
      });
    }

    try {
      final token = await _authService.getToken();
      final bookmarks = await _apiService.getUserBookmarks(
        skip: _currentPage * _pageSize,
        limit: _pageSize,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        if (loadMore) {
          _bookmarkedPosts.addAll(bookmarks);
        } else {
          _bookmarkedPosts = bookmarks;
        }
        _currentPage++;
        _isLoading = false;
        _isLoadingMore = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _isLoadingMore = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load bookmarks: $e')),
      );
    }
  }

  Future<void> _loadStats() async {
    try {
      final token = await _authService.getToken();
      final stats = await _apiService.getUserBookmarkStats(
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        _stats = stats;
      });
    } catch (e) {
      print('Error loading bookmark stats: $e');
    }
  }

  Future<void> _removeBookmark(BlogPost post) async {
    try {
      final token = await _authService.getToken();
      await _apiService.removeBookmark(
        post.id!,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        _bookmarkedPosts.removeWhere((p) => p.id == post.id);
      });
      
      // Update stats
      _loadStats();
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Removed "${post.title}" from bookmarks'),
          action: SnackBarAction(
            label: 'Undo',
            onPressed: () => _addBookmark(post),
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to remove bookmark: $e')),
      );
    }
  }

  Future<void> _addBookmark(BlogPost post) async {
    try {
      final token = await _authService.getToken();
      await _apiService.bookmarkPost(
        post.id!,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      // Reload bookmarks to get updated list
      _loadBookmarks();
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Added "${post.title}" to bookmarks')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to add bookmark: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bookmarks'),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => _loadBookmarks(),
          ),
        ],
      ),
      body: Column(
        children: [
          // Stats header
          if (_stats != null)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
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
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.bookmark,
                        color: Theme.of(context).primaryColor,
                        size: 24,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        '${_stats!.totalBookmarks} Saved Posts',
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  if (_stats!.totalBookmarks > 0) ...[
                    const SizedBox(height: 8),
                    Text(
                      'Your personal collection of saved articles',
                      style: TextStyle(
                        color: Colors.grey[600],
                        fontSize: 14,
                      ),
                    ),
                  ],
                ],
              ),
            ),
          
          // Bookmarked posts list
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _bookmarkedPosts.isEmpty
                    ? _buildEmptyState()
                    : RefreshIndicator(
                        onRefresh: () => _loadBookmarks(),
                        child: ListView.builder(
                          padding: const EdgeInsets.all(16),
                          itemCount: _bookmarkedPosts.length + (_isLoadingMore ? 1 : 0),
                          itemBuilder: (context, index) {
                            if (index == _bookmarkedPosts.length) {
                              // Load more indicator
                              return const Center(
                                child: Padding(
                                  padding: EdgeInsets.all(16),
                                  child: CircularProgressIndicator(),
                                ),
                              );
                            }
                            
                            final post = _bookmarkedPosts[index];
                            return Dismissible(
                              key: Key('bookmark_${post.id}'),
                              direction: DismissDirection.endToStart,
                              background: Container(
                                alignment: Alignment.centerRight,
                                padding: const EdgeInsets.only(right: 20),
                                decoration: BoxDecoration(
                                  color: Colors.red,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: const Icon(
                                  Icons.bookmark_remove,
                                  color: Colors.white,
                                  size: 24,
                                ),
                              ),
                              confirmDismiss: (direction) async {
                                return await showDialog<bool>(
                                  context: context,
                                  builder: (context) => AlertDialog(
                                    title: const Text('Remove Bookmark'),
                                    content: Text(
                                      'Remove "${post.title}" from your bookmarks?',
                                    ),
                                    actions: [
                                      TextButton(
                                        onPressed: () => Navigator.of(context).pop(false),
                                        child: const Text('Cancel'),
                                      ),
                                      ElevatedButton(
                                        onPressed: () => Navigator.of(context).pop(true),
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Colors.red,
                                        ),
                                        child: const Text('Remove'),
                                      ),
                                    ],
                                  ),
                                );
                              },
                              onDismissed: (direction) => _removeBookmark(post),
                              child: BlogPostCard(
                                blogPost: post,
                                onTap: () {
                                  // Navigate to blog detail
                                },
                                trailing: IconButton(
                                  icon: const Icon(Icons.bookmark_remove),
                                  onPressed: () => _removeBookmark(post),
                                  color: Colors.red,
                                ),
                              ),
                            );
                            
                            // Load more when reaching the end
                            if (index == _bookmarkedPosts.length - 5 && !_isLoadingMore) {
                              _loadBookmarks(loadMore: true);
                            }
                          },
                        ),
                      ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.bookmark_border,
              size: 80,
              color: Colors.grey[400],
            ),
            const SizedBox(height: 24),
            const Text(
              'No Bookmarks Yet',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              'Save articles you want to read later by bookmarking them',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 32),
            ElevatedButton.icon(
              onPressed: () {
                // Navigate to blog list or search
                Navigator.of(context).pop();
              },
              icon: const Icon(Icons.explore),
              label: const Text('Explore Posts'),
            ),
          ],
        ),
      ),
    );
  }
}

// Helper widget to add bookmark functionality to blog post cards
class BookmarkButton extends StatefulWidget {
  final BlogPost post;
  final ApiService apiService;
  final AuthService authService;
  final VoidCallback? onBookmarkChanged;

  const BookmarkButton({
    Key? key,
    required this.post,
    required this.apiService,
    required this.authService,
    this.onBookmarkChanged,
  }) : super(key: key);

  @override
  State<BookmarkButton> createState() => _BookmarkButtonState();
}

class _BookmarkButtonState extends State<BookmarkButton> {
  bool _isBookmarked = false;
  bool _isLoading = false;
  int _bookmarkCount = 0;

  @override
  void initState() {
    super.initState();
    _loadBookmarkStatus();
  }

  Future<void> _loadBookmarkStatus() async {
    try {
      final token = await widget.authService.getToken();
      final stats = await widget.apiService.getPostBookmarkStats(
        widget.post.id!,
        headers: {'Authorization': 'Bearer $token'},
      );
      
      setState(() {
        _isBookmarked = stats.isBookmarked ?? false;
        _bookmarkCount = stats.totalBookmarks;
      });
    } catch (e) {
      print('Error loading bookmark status: $e');
    }
  }

  Future<void> _toggleBookmark() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final token = await widget.authService.getToken();
      
      if (_isBookmarked) {
        await widget.apiService.removeBookmark(
          widget.post.id!,
          headers: {'Authorization': 'Bearer $token'},
        );
      } else {
        await widget.apiService.bookmarkPost(
          widget.post.id!,
          headers: {'Authorization': 'Bearer $token'},
        );
      }
      
      setState(() {
        _isBookmarked = !_isBookmarked;
        _bookmarkCount += _isBookmarked ? 1 : -1;
      });
      
      widget.onBookmarkChanged?.call();
      
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Bookmark action failed: $e')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        IconButton(
          onPressed: _isLoading ? null : _toggleBookmark,
          icon: _isLoading
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : Icon(
                  _isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                  color: _isBookmarked ? Theme.of(context).primaryColor : null,
                ),
        ),
        if (_bookmarkCount > 0)
          Text(
            _bookmarkCount.toString(),
            style: const TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.bold,
            ),
          ),
      ],
    );
  }
}