'use client';

import { useEffect, useState } from 'react';
import { adminAPI } from '@/lib/api';
import { formatNumber, formatRelativeTime } from '@/lib/admin';

interface ContentAnalytics {
  total_posts: number;
  recent_posts: number;
  total_comments: number;
  recent_comments: number;
  top_authors_by_posts: Array<{username: string; name: string; count: number}>;
  top_authors_by_comments: Array<{username: string; name: string; count: number}>;
  period_days: number;
}

export default function AdminAnalyticsPage() {
  const [analytics, setAnalytics] = useState<ContentAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [period, setPeriod] = useState(30);

  useEffect(() => {
    loadAnalytics();
  }, [period]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const data = await adminAPI.getContentAnalytics(period);
      setAnalytics(data);
    } catch (err) {
      console.error('Failed to load analytics:', err);
      setError('Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
        <div className="animate-pulse">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-gray-200 h-32 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
          <button
            onClick={loadAnalytics}
            className="mt-2 text-red-600 hover:text-red-800 font-medium"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const periodOptions = [
    { value: 7, label: 'Last 7 days' },
    { value: 30, label: 'Last 30 days' },
    { value: 90, label: 'Last 3 months' },
    { value: 365, label: 'Last year' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
        <div className="flex items-center space-x-4">
          <select
            value={period}
            onChange={(e) => setPeriod(Number(e.target.value))}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          >
            {periodOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <button
            onClick={loadAnalytics}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600">Total Posts</p>
              <p className="text-3xl font-bold text-gray-900">{formatNumber(analytics?.total_posts || 0)}</p>
              <p className="text-sm text-green-600">+{analytics?.recent_posts || 0} recent</p>
            </div>
            <div className="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center">
              <span className="text-2xl">📝</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600">Total Comments</p>
              <p className="text-3xl font-bold text-gray-900">{formatNumber(analytics?.total_comments || 0)}</p>
              <p className="text-sm text-green-600">+{analytics?.recent_comments || 0} recent</p>
            </div>
            <div className="w-12 h-12 bg-purple-50 rounded-lg flex items-center justify-center">
              <span className="text-2xl">💬</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600">Growth Rate</p>
              <p className="text-3xl font-bold text-gray-900">
                {analytics?.total_posts ? ((analytics.recent_posts / analytics.total_posts) * 100).toFixed(1) : 0}%
              </p>
              <p className="text-sm text-gray-500">Posts in period</p>
            </div>
            <div className="w-12 h-12 bg-green-50 rounded-lg flex items-center justify-center">
              <span className="text-2xl">📈</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-600">Engagement</p>
              <p className="text-3xl font-bold text-gray-900">
                {analytics?.total_posts ? (analytics.total_comments / analytics.total_posts).toFixed(1) : 0}
              </p>
              <p className="text-sm text-gray-500">Comments per post</p>
            </div>
            <div className="w-12 h-12 bg-orange-50 rounded-lg flex items-center justify-center">
              <span className="text-2xl">🔥</span>
            </div>
          </div>
        </div>
      </div>

      {/* Top Authors */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Authors by Posts */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Authors by Posts</h3>
          {analytics?.top_authors_by_posts?.length ? (
            <div className="space-y-3">
              {analytics.top_authors_by_posts.map((author, index) => (
                <div key={author.username} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-indigo-500 rounded-full flex items-center justify-center mr-3">
                      <span className="text-white text-sm font-medium">
                        {author.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{author.name}</p>
                      <p className="text-xs text-gray-500">@{author.username}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-gray-900">{author.count}</p>
                    <p className="text-xs text-gray-500">posts</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500">No data available</p>
            </div>
          )}
        </div>

        {/* Top Authors by Comments */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Authors by Comments</h3>
          {analytics?.top_authors_by_comments?.length ? (
            <div className="space-y-3">
              {analytics.top_authors_by_comments.map((author, index) => (
                <div key={author.username} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center mr-3">
                      <span className="text-white text-sm font-medium">
                        {author.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{author.name}</p>
                      <p className="text-xs text-gray-500">@{author.username}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-gray-900">{author.count}</p>
                    <p className="text-xs text-gray-500">comments</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500">No data available</p>
            </div>
          )}
        </div>
      </div>

      {/* Content Insights */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Content Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <p className="text-3xl font-bold text-indigo-600">
              {analytics?.recent_posts || 0}
            </p>
            <p className="text-sm text-gray-600 mt-1">
              New posts in last {period} days
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {period > 7 ? `~${(analytics?.recent_posts || 0) / (period / 7)} per week` : ''}
            </p>
          </div>
          
          <div className="text-center">
            <p className="text-3xl font-bold text-purple-600">
              {analytics?.recent_comments || 0}
            </p>
            <p className="text-sm text-gray-600 mt-1">
              New comments in last {period} days
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {period > 7 ? `~${(analytics?.recent_comments || 0) / (period / 7)} per week` : ''}
            </p>
          </div>
          
          <div className="text-center">
            <p className="text-3xl font-bold text-green-600">
              {analytics?.top_authors_by_posts?.length || 0}
            </p>
            <p className="text-sm text-gray-600 mt-1">
              Active authors
            </p>
            <p className="text-xs text-gray-500 mt-1">
              With published content
            </p>
          </div>
        </div>
      </div>

      {/* Period Summary */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg p-6 text-white">
        <h3 className="text-xl font-semibold mb-2">Analytics Summary</h3>
        <p className="text-indigo-100 text-sm">
          Over the last {period} days, your blog has seen{' '}
          <strong>{analytics?.recent_posts || 0} new posts</strong> and{' '}
          <strong>{analytics?.recent_comments || 0} new comments</strong>, 
          indicating {analytics?.recent_posts && analytics.recent_posts > 0 ? 'active' : 'low'} content creation 
          and {analytics?.recent_comments && analytics.recent_comments > 0 ? 'strong' : 'limited'} community engagement.
        </p>
      </div>
    </div>
  );
}