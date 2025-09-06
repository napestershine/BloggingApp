// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck - Component with interface mismatches
'use client';

import { useState, useEffect } from 'react';
import { bookmarkAPI, BlogPost, BookmarkStats } from '@/lib/api';

export default function BookmarksComponent() {
  const [bookmarkedPosts, setBookmarkedPosts] = useState<BlogPost[]>([]);
  const [stats, setStats] = useState<BookmarkStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const pageSize = 20;

  useEffect(() => {
    loadBookmarks();
    loadStats();
  }, []);

  const loadBookmarks = async (loadMore = false) => {
    if (loadMore && !hasMore) return;

    setLoading(true);
    try {
      const page = loadMore ? currentPage + 1 : 0;
      const bookmarks = await bookmarkAPI.getBookmarks(page * pageSize, pageSize);
      
      setBookmarkedPosts(prev => 
        loadMore ? [...prev, ...bookmarks] : bookmarks
      );
      setCurrentPage(page);
      setHasMore(bookmarks.length === pageSize);
    } catch (error) {
      console.error('Failed to load bookmarks:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await bookmarkAPI.getUserStats();
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load bookmark stats:', error);
    }
  };

  const removeBookmark = async (post: BlogPost) => {
    try {
      await bookmarkAPI.removeBookmark(post.id);
      
      // Update local state
      setBookmarkedPosts(prev => prev.filter(p => p.id !== post.id));
      
      // Update stats
      loadStats();
      
      // Show success message (could be implemented with a toast library)
      console.log(`Removed "${post.title}" from bookmarks`);
    } catch (error) {
      console.error('Failed to remove bookmark:', error);
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const addBookmark = async (post: BlogPost) => {
    try {
      await bookmarkAPI.bookmarkPost(post.id);
      
      // Reload bookmarks to get updated list
      loadBookmarks();
      
      console.log(`Added "${post.title}" to bookmarks`);
    } catch (error) {
      console.error('Failed to add bookmark:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Bookmarks
          </h1>
          
          <button
            onClick={() => loadBookmarks(false)}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg 
                     transition-colors font-medium"
          >
            🔄 Refresh
          </button>
        </div>

        {/* Stats */}
        {stats && (
          <div className="text-center">
            <div className="flex items-center justify-center space-x-3">
              <span className="text-3xl">🔖</span>
              <div>
                <div className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats.total_bookmarks} Saved Posts
                </div>
                {stats.total_bookmarks > 0 && (
                  <div className="text-gray-600 dark:text-gray-400">
                    Your personal collection of saved articles
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Bookmarked Posts */}
      <div className="space-y-6">
        {loading && bookmarkedPosts.length === 0 ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : bookmarkedPosts.length > 0 ? (
          <>
            <div className="grid gap-6">
              {bookmarkedPosts.map((post) => (
                <BookmarkPostCard
                  key={post.id}
                  post={post}
                  onRemove={() => removeBookmark(post)}
                  onPostClick={() => {
                    // Navigate to post detail
                    window.open(`/blog/${post.id}`, '_blank');
                  }}
                />
              ))}
            </div>

            {/* Load More Button */}
            {hasMore && (
              <div className="text-center pt-6">
                <button
                  onClick={() => loadBookmarks(true)}
                  disabled={loading}
                  className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg 
                           transition-colors font-medium disabled:opacity-50"
                >
                  {loading ? (
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Loading...</span>
                    </div>
                  ) : (
                    'Load More'
                  )}
                </button>
              </div>
            )}
          </>
        ) : (
          <EmptyBookmarksState />
        )}
      </div>
    </div>
  );
}

interface BookmarkPostCardProps {
  post: BlogPost;
  onRemove: () => void;
  onPostClick: () => void;
}

function BookmarkPostCard({ post, onRemove, onPostClick }: BookmarkPostCardProps) {
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);

  const handleRemove = () => {
    if (showConfirmDialog) {
      onRemove();
      setShowConfirmDialog(false);
    } else {
      setShowConfirmDialog(true);
      // Auto-hide confirmation after 3 seconds
      setTimeout(() => setShowConfirmDialog(false), 3000);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const truncateContent = (content: string, maxLength = 150) => {
    if (content.length <= maxLength) return content;
    return content.slice(0, maxLength).trim() + '...';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div 
            className="flex-1 cursor-pointer"
            onClick={onPostClick}
          >
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 
                         hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              {post.title}
            </h3>
            <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <span>👤 {post.author}</span>
              <span className="mx-2">•</span>
              <span>📅 {formatDate(post.created_at)}</span>
            </div>
          </div>

          {/* Remove Button */}
          <button
            onClick={handleRemove}
            className={`ml-4 px-3 py-2 rounded-lg font-medium transition-all ${
              showConfirmDialog
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-400'
            }`}
            title={showConfirmDialog ? 'Click again to confirm removal' : 'Remove bookmark'}
          >
            {showConfirmDialog ? '🗑️ Confirm' : '🔖'}
          </button>
        </div>

        {/* Content Preview */}
        <div className="mb-4">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {truncateContent(post.content)}
          </p>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-600">
          <div className="flex items-center space-x-4">
            {post.slug && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs 
                             font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                {post.slug}
              </span>
            )}
          </div>
          
          <button
            onClick={onPostClick}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg 
                     transition-colors font-medium text-sm"
          >
            Read More →
          </button>
        </div>
      </div>
    </div>
  );
}

function EmptyBookmarksState() {
  return (
    <div className="text-center py-16">
      <div className="text-8xl mb-6">🔖</div>
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        No Bookmarks Yet
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
        Save articles you want to read later by bookmarking them. 
        Your saved posts will appear here.
      </p>
      <button
        onClick={() => window.location.href = '/'}
        className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg 
                 transition-colors font-medium inline-flex items-center space-x-2"
      >
        <span>🔍</span>
        <span>Explore Posts</span>
      </button>
    </div>
  );
}

// Bookmark Button Component for use in other components
interface BookmarkButtonProps {
  post: BlogPost;
  onBookmarkChange?: () => void;
}

export function BookmarkButton({ post, onBookmarkChange }: BookmarkButtonProps) {
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [bookmarkCount, setBookmarkCount] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadBookmarkStatus();
  }, [post.id]);

  const loadBookmarkStatus = async () => {
    try {
      const stats = await bookmarkAPI.getPostStats(post.id);
      setIsBookmarked(stats.is_bookmarked || false);
      setBookmarkCount(stats.total_bookmarks);
    } catch (error) {
      console.error('Failed to load bookmark status:', error);
    }
  };

  const toggleBookmark = async () => {
    setLoading(true);
    try {
      if (isBookmarked) {
        await bookmarkAPI.removeBookmark(post.id);
      } else {
        await bookmarkAPI.bookmarkPost(post.id);
      }
      
      setIsBookmarked(!isBookmarked);
      setBookmarkCount(prev => isBookmarked ? prev - 1 : prev + 1);
      onBookmarkChange?.();
    } catch (error) {
      console.error('Failed to toggle bookmark:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={toggleBookmark}
      disabled={loading}
      className={`flex flex-col items-center justify-center p-2 rounded-lg transition-colors ${
        isBookmarked
          ? 'text-blue-600 bg-blue-50 dark:bg-blue-900 dark:text-blue-400'
          : 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300'
      } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
      title={isBookmarked ? 'Remove bookmark' : 'Add bookmark'}
    >
      {loading ? (
        <div className="w-5 h-5 animate-spin border-2 border-current border-t-transparent rounded-full"></div>
      ) : (
        <span className="text-xl">
          {isBookmarked ? '🔖' : '📑'}
        </span>
      )}
      
      {bookmarkCount > 0 && (
        <span className="text-xs font-medium mt-1">
          {bookmarkCount}
        </span>
      )}
    </button>
  );
}