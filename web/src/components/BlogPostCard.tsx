'use client';

import { BlogPost } from '@/types';

interface BlogPostCardProps {
  post: BlogPost;
  onClick?: () => void;
  showActions?: boolean;
}

export default function BlogPostCard({ 
  post, 
  onClick, 
  showActions = true 
}: BlogPostCardProps) {
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
    <div 
      className={`bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg 
                  transition-shadow duration-200 border border-gray-200 dark:border-gray-700
                  ${onClick ? 'cursor-pointer' : ''}`}
      onClick={onClick}
    >
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 
                         hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              {post.title}
            </h3>
            <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <span className="flex items-center">
                👤 {post.author}
              </span>
              <span className="mx-2">•</span>
              <span className="flex items-center">
                📅 {formatDate(post.created_at)}
              </span>
            </div>
          </div>
        </div>

        {/* Content Preview */}
        <div className="mb-4">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {truncateContent(post.content)}
          </p>
        </div>

        {/* Footer */}
        {showActions && (
          <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-600">
            <div className="flex items-center space-x-4">
              {post.slug && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs 
                               font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                  {post.slug}
                </span>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  // Handle share
                }}
                className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 
                         hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors"
                title="Share"
              >
                🔗
              </button>
              
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  // Handle bookmark
                }}
                className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 
                         hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors"
                title="Bookmark"
              >
                🔖
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}