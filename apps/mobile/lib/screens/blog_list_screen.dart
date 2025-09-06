import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';

import '../models/blog_post.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import '../widgets/blog_post_card.dart';
import '../widgets/skeleton_loader.dart';
import '../widgets/error_display.dart';
import '../utils/responsive_layout.dart';

class BlogListScreen extends StatefulWidget {
  const BlogListScreen({super.key});

  @override
  State<BlogListScreen> createState() => _BlogListScreenState();
}

class _BlogListScreenState extends State<BlogListScreen> {
  List<BlogPost> _blogPosts = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadBlogPosts();
  }

  Future<void> _loadBlogPosts() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final authService = Provider.of<AuthService>(context, listen: false);
      final apiService = Provider.of<ApiService>(context, listen: false);
      
      final blogPosts = await apiService.getBlogPosts(
        headers: authService.getAuthHeaders(),
      );
      
      setState(() {
        _blogPosts = blogPosts;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _logout() async {
    final authService = Provider.of<AuthService>(context, listen: false);
    await authService.logout();
    if (mounted) {
      context.go('/login');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Blog Posts'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadBlogPosts,
          ),
          PopupMenuButton(
            onSelected: (value) {
              if (value == 'logout') {
                _logout();
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    Icon(Icons.logout),
                    SizedBox(width: 8),
                    Text('Logout'),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: _buildBody(),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.go('/create-post'),
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: 6, // Show 6 skeleton items
        itemBuilder: (context, index) => const BlogPostSkeleton(),
      );
    }

    if (_error != null) {
      return ErrorDisplay(
        message: _error!,
        onRetry: _loadBlogPosts,
      );
    }

    if (_blogPosts.isEmpty) {
      return EmptyStateDisplay(
        title: 'No blog posts yet',
        message: 'Be the first to create a blog post!',
        icon: Icons.article_outlined,
        action: ElevatedButton.icon(
          onPressed: () => context.go('/create-post'),
          icon: const Icon(Icons.add),
          label: const Text('Create Post'),
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _loadBlogPosts,
      child: ResponsiveWidth.centered(
        context,
        ResponsiveLayout(
          mobile: _buildMobileList(),
          tablet: _buildTabletGrid(),
          desktop: _buildDesktopGrid(),
        ),
      ),
    );
  }

  Widget _buildMobileList() {
    return ListView.builder(
      padding: ResponsivePadding.page(context),
      itemCount: _blogPosts.length,
      itemBuilder: (context, index) {
        final blogPost = _blogPosts[index];
        return BlogPostCard(
          blogPost: blogPost,
          onTap: () => context.go('/blog/${blogPost.id}'),
        );
      },
    );
  }

  Widget _buildTabletGrid() {
    return GridView.builder(
      padding: ResponsivePadding.page(context),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: ResponsiveGrid.spacing(context),
        mainAxisSpacing: ResponsiveGrid.spacing(context),
        childAspectRatio: 1.2,
      ),
      itemCount: _blogPosts.length,
      itemBuilder: (context, index) {
        final blogPost = _blogPosts[index];
        return BlogPostCard(
          blogPost: blogPost,
          onTap: () => context.go('/blog/${blogPost.id}'),
          isCompact: true,
        );
      },
    );
  }

  Widget _buildDesktopGrid() {
    return GridView.builder(
      padding: ResponsivePadding.page(context),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: ResponsiveGrid.spacing(context),
        mainAxisSpacing: ResponsiveGrid.spacing(context),
        childAspectRatio: 1.2,
      ),
      itemCount: _blogPosts.length,
      itemBuilder: (context, index) {
        final blogPost = _blogPosts[index];
        return BlogPostCard(
          blogPost: blogPost,
          onTap: () => context.go('/blog/${blogPost.id}'),
          isCompact: true,
        );
      },
    );
  }
}