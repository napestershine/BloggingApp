// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck - Component with interface mismatches
'use client';

import { useState, useEffect, useCallback } from 'react';
import { 
  searchAPI, 
  SearchSuggestion, 
  SearchFilters, 
  BlogPost 
} from '@/lib/api';
import BlogPostCard from './BlogPostCard';

interface SearchComponentProps {
  onPostSelect?: (post: BlogPost) => void;
}

// Simple debounce implementation
function debounce<T extends (...args: any[]) => any>(func: T, wait: number): T {
  let timeout: NodeJS.Timeout;
  return ((...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  }) as T;
}


export default function SearchComponent({ onPostSelect }: SearchComponentProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<BlogPost[]>([]);
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [filters, setFilters] = useState<SearchFilters | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedTag, setSelectedTag] = useState<string>('');
  const [selectedAuthor, setSelectedAuthor] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Load filters on component mount
  useEffect(() => {
    const loadFilters = async () => {
      try {
        const filtersData = await searchAPI.getFilters();
        setFilters(filtersData);
      } catch (error) {
        console.error('Failed to load search filters:', error);
      }
    };
    loadFilters();
  }, []);

  // Debounced function to get suggestions
  const debouncedGetSuggestions = useCallback(
    debounce(async (searchQuery: string) => {
      if (searchQuery.length >= 2) {
        try {
          const suggestionResults = await searchAPI.getSuggestions(searchQuery);
          setSuggestions(suggestionResults);
          setShowSuggestions(true);
        } catch (error) {
          console.error('Failed to get suggestions:', error);
          setSuggestions([]);
        }
      } else {
        setSuggestions([]);
        setShowSuggestions(false);
      }
    }, 300),
    []
  );

  // Handle query change
  const handleQueryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newQuery = e.target.value;
    setQuery(newQuery);
    debouncedGetSuggestions(newQuery);
  };

  // Perform search
  const performSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setShowSuggestions(false);

    try {
      const searchResults = await searchAPI.searchPosts({
        q: query,
        category: selectedCategory || undefined,
        tag: selectedTag || undefined,
        author: selectedAuthor || undefined,
      });
      setResults(searchResults);
    } catch (error) {
      console.error('Search failed:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    performSearch();
  };

  // Apply suggestion
  const applySuggestion = (suggestion: SearchSuggestion) => {
    setQuery(suggestion.text);
    setShowSuggestions(false);
    // Trigger search with the suggestion
    setTimeout(performSearch, 100);
  };

  // Clear filters
  const clearFilters = () => {
    setSelectedCategory('');
    setSelectedTag('');
    setSelectedAuthor('');
    if (query) {
      performSearch();
    }
  };

  // Get icon for suggestion type
  const getSuggestionIcon = (type: string) => {
    switch (type) {
      case 'title':
        return '📄';
      case 'category':
        return '📁';
      case 'tag':
        return '🏷️';
      case 'author':
        return '👤';
      default:
        return '🔍';
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6">
      {/* Search Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Search Posts
        </h1>

        {/* Search Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Search Input */}
          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={handleQueryChange}
              placeholder="Search posts..."
              className="w-full px-4 py-3 pr-12 border border-gray-300 dark:border-gray-600 
                       rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
            <button
              type="submit"
              className="absolute right-3 top-1/2 transform -translate-y-1/2
                       text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              🔍
            </button>
            
            {query && (
              <button
                type="button"
                onClick={() => {
                  setQuery('');
                  setResults([]);
                  setSuggestions([]);
                  setShowSuggestions(false);
                }}
                className="absolute right-12 top-1/2 transform -translate-y-1/2
                         text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                ✕
              </button>
            )}
          </div>

          {/* Suggestions */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="absolute z-10 w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 
                          rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => applySuggestion(suggestion)}
                  className="w-full text-left px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700
                           flex items-center space-x-3 border-b border-gray-200 dark:border-gray-600 last:border-b-0"
                >
                  <span className="text-lg">{getSuggestionIcon(suggestion.type)}</span>
                  <div>
                    <div className="font-medium text-gray-900 dark:text-white">
                      {suggestion.text}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      {suggestion.description}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}

          {/* Filters */}
          {filters && (
            <div className="flex flex-wrap gap-3">
              {/* Category Filter */}
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                         bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">All Categories</option>
                {filters.categories.map((category) => (
                  <option key={category.slug} value={category.name}>
                    {category.name}
                  </option>
                ))}
              </select>

              {/* Tag Filter */}
              <select
                value={selectedTag}
                onChange={(e) => setSelectedTag(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                         bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">All Tags</option>
                {filters.tags.slice(0, 10).map((tag) => (
                  <option key={tag.name} value={tag.name}>
                    {tag.name} ({tag.post_count})
                  </option>
                ))}
              </select>

              {/* Author Filter */}
              <select
                value={selectedAuthor}
                onChange={(e) => setSelectedAuthor(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                         bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">All Authors</option>
                {filters.authors.slice(0, 10).map((author) => (
                  <option key={author.username} value={author.username}>
                    {author.username} ({author.post_count})
                  </option>
                ))}
              </select>

              {/* Clear Filters */}
              {(selectedCategory || selectedTag || selectedAuthor) && (
                <button
                  type="button"
                  onClick={clearFilters}
                  className="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300
                           rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors"
                >
                  Clear Filters
                </button>
              )}
            </div>
          )}
        </form>
      </div>

      {/* Search Results */}
      <div className="space-y-6">
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : results.length > 0 ? (
          <>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Search Results ({results.length})
            </h2>
            <div className="grid gap-6">
              {results.map((post) => (
                <BlogPostCard
                  key={post.id}
                  post={post}
                  onClick={() => onPostSelect?.(post)}
                />
              ))}
            </div>
          </>
        ) : query && !loading ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              No posts found
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Try adjusting your search terms or filters
            </p>
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Start searching
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Enter a search term to find posts
            </p>
          </div>
        )}
      </div>
    </div>
  );
}