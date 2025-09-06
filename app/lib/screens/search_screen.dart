import 'package:flutter/material.dart';
import '../models/blog_post.dart';
import '../models/search_result.dart';
import '../services/api_service.dart';
import '../widgets/blog_post_card.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({Key? key}) : super(key: key);

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _searchController = TextEditingController();
  final _apiService = ApiService();
  
  List<BlogPost> _searchResults = [];
  List<SearchSuggestion> _suggestions = [];
  SearchFilters? _filters;
  
  bool _isLoading = false;
  bool _showSuggestions = false;
  String? _selectedCategory;
  String? _selectedTag;
  String? _selectedAuthor;

  @override
  void initState() {
    super.initState();
    _loadFilters();
    _searchController.addListener(_onSearchChanged);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _onSearchChanged() {
    final query = _searchController.text;
    if (query.isNotEmpty && query.length >= 2) {
      _getSuggestions(query);
    } else {
      setState(() {
        _suggestions = [];
        _showSuggestions = false;
      });
    }
  }

  Future<void> _loadFilters() async {
    try {
      final filters = await _apiService.getSearchFilters();
      setState(() {
        _filters = filters;
      });
    } catch (e) {
      print('Error loading filters: $e');
    }
  }

  Future<void> _getSuggestions(String query) async {
    try {
      final suggestions = await _apiService.getSearchSuggestions(query: query);
      setState(() {
        _suggestions = suggestions;
        _showSuggestions = true;
      });
    } catch (e) {
      print('Error getting suggestions: $e');
    }
  }

  Future<void> _performSearch() async {
    final query = _searchController.text.trim();
    if (query.isEmpty) return;

    setState(() {
      _isLoading = true;
      _showSuggestions = false;
    });

    try {
      final results = await _apiService.searchPosts(
        query: query,
        category: _selectedCategory,
        tag: _selectedTag,
        author: _selectedAuthor,
      );
      
      setState(() {
        _searchResults = results;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Search failed: $e')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _clearFilters() {
    setState(() {
      _selectedCategory = null;
      _selectedTag = null;
      _selectedAuthor = null;
    });
    if (_searchController.text.isNotEmpty) {
      _performSearch();
    }
  }

  void _applySuggestion(SearchSuggestion suggestion) {
    _searchController.text = suggestion.text;
    setState(() {
      _showSuggestions = false;
    });
    _performSearch();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Search Posts'),
        elevation: 0,
      ),
      body: Column(
        children: [
          // Search bar and filters
          Container(
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
                // Search input
                TextField(
                  controller: _searchController,
                  decoration: InputDecoration(
                    hintText: 'Search posts...',
                    prefixIcon: const Icon(Icons.search),
                    suffixIcon: _searchController.text.isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () {
                              _searchController.clear();
                              setState(() {
                                _searchResults = [];
                                _suggestions = [];
                                _showSuggestions = false;
                              });
                            },
                          )
                        : null,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                  onSubmitted: (_) => _performSearch(),
                ),
                const SizedBox(height: 12),
                
                // Filter chips
                if (_filters != null) ...[
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        // Category filter
                        PopupMenuButton<String>(
                          child: Chip(
                            label: Text(_selectedCategory ?? 'Category'),
                            backgroundColor: _selectedCategory != null
                                ? Theme.of(context).primaryColor.withOpacity(0.2)
                                : null,
                          ),
                          itemBuilder: (context) => [
                            const PopupMenuItem(
                              value: null,
                              child: Text('All Categories'),
                            ),
                            ..._filters!.categories.map((category) =>
                                PopupMenuItem(
                                  value: category.name,
                                  child: Text(category.name),
                                )),
                          ],
                          onSelected: (value) {
                            setState(() {
                              _selectedCategory = value;
                            });
                            if (_searchController.text.isNotEmpty) {
                              _performSearch();
                            }
                          },
                        ),
                        const SizedBox(width: 8),
                        
                        // Tag filter
                        PopupMenuButton<String>(
                          child: Chip(
                            label: Text(_selectedTag ?? 'Tag'),
                            backgroundColor: _selectedTag != null
                                ? Theme.of(context).primaryColor.withOpacity(0.2)
                                : null,
                          ),
                          itemBuilder: (context) => [
                            const PopupMenuItem(
                              value: null,
                              child: Text('All Tags'),
                            ),
                            ..._filters!.tags.take(10).map((tag) =>
                                PopupMenuItem(
                                  value: tag.name,
                                  child: Text('${tag.name} (${tag.postCount})'),
                                )),
                          ],
                          onSelected: (value) {
                            setState(() {
                              _selectedTag = value;
                            });
                            if (_searchController.text.isNotEmpty) {
                              _performSearch();
                            }
                          },
                        ),
                        const SizedBox(width: 8),
                        
                        // Author filter
                        PopupMenuButton<String>(
                          child: Chip(
                            label: Text(_selectedAuthor ?? 'Author'),
                            backgroundColor: _selectedAuthor != null
                                ? Theme.of(context).primaryColor.withOpacity(0.2)
                                : null,
                          ),
                          itemBuilder: (context) => [
                            const PopupMenuItem(
                              value: null,
                              child: Text('All Authors'),
                            ),
                            ..._filters!.authors.take(10).map((author) =>
                                PopupMenuItem(
                                  value: author.username,
                                  child: Text('${author.username} (${author.postCount})'),
                                )),
                          ],
                          onSelected: (value) {
                            setState(() {
                              _selectedAuthor = value;
                            });
                            if (_searchController.text.isNotEmpty) {
                              _performSearch();
                            }
                          },
                        ),
                        
                        // Clear filters button
                        if (_selectedCategory != null || _selectedTag != null || _selectedAuthor != null) ...[
                          const SizedBox(width: 8),
                          ActionChip(
                            label: const Text('Clear'),
                            onPressed: _clearFilters,
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
          
          // Suggestions
          if (_showSuggestions && _suggestions.isNotEmpty)
            Container(
              constraints: const BoxConstraints(maxHeight: 200),
              child: Card(
                margin: const EdgeInsets.symmetric(horizontal: 16),
                child: ListView.builder(
                  shrinkWrap: true,
                  itemCount: _suggestions.length,
                  itemBuilder: (context, index) {
                    final suggestion = _suggestions[index];
                    return ListTile(
                      leading: Icon(_getIconForSuggestionType(suggestion.type)),
                      title: Text(suggestion.text),
                      subtitle: Text(suggestion.description),
                      onTap: () => _applySuggestion(suggestion),
                    );
                  },
                ),
              ),
            ),
          
          // Results
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _searchResults.isEmpty && _searchController.text.isNotEmpty
                    ? const Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.search_off, size: 64, color: Colors.grey),
                            SizedBox(height: 16),
                            Text(
                              'No posts found',
                              style: TextStyle(fontSize: 18, color: Colors.grey),
                            ),
                          ],
                        ),
                      )
                    : _searchResults.isEmpty
                        ? const Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.search, size: 64, color: Colors.grey),
                                SizedBox(height: 16),
                                Text(
                                  'Start typing to search posts...',
                                  style: TextStyle(fontSize: 18, color: Colors.grey),
                                ),
                              ],
                            ),
                          )
                        : ListView.builder(
                            padding: const EdgeInsets.all(16),
                            itemCount: _searchResults.length,
                            itemBuilder: (context, index) {
                              return BlogPostCard(
                                blogPost: _searchResults[index],
                                onTap: () {
                                  // Navigate to blog detail
                                },
                              );
                            },
                          ),
          ),
        ],
      ),
    );
  }

  IconData _getIconForSuggestionType(String type) {
    switch (type) {
      case 'title':
        return Icons.article;
      case 'category':
        return Icons.category;
      case 'tag':
        return Icons.label;
      case 'author':
        return Icons.person;
      default:
        return Icons.search;
    }
  }
}