'use client';

import { useEffect, useState } from 'react';
import { adminAPI } from '@/lib/api';
import { AdminStats } from '@/types';
import { formatNumber, formatRelativeTime } from '@/lib/admin';

export default function AdminDashboard() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await adminAPI.getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load dashboard stats:', err);
      setError('Failed to load dashboard statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
          <button
            onClick={loadDashboardStats}
            className="mt-2 text-red-600 hover:text-red-800 font-medium"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Users',
      value: stats?.total_users || 0,
      icon: '👥',
      color: 'blue',
      change: `+${stats?.new_users_today || 0} today`,
    },
    {
      title: 'Total Posts',
      value: stats?.total_posts || 0,
      icon: '📝',
      color: 'green',
      change: `+${stats?.new_posts_today || 0} today`,
    },
    {
      title: 'Total Comments',
      value: stats?.total_comments || 0,
      icon: '💬',
      color: 'purple',
      change: `+${stats?.new_comments_today || 0} today`,
    },
    {
      title: 'Admin Users',
      value: stats?.admin_users || 0,
      icon: '⚡',
      color: 'orange',
      change: 'Active admins',
    },
  ];

  const getCardColorClasses = (color: string) => {
    switch (color) {
      case 'blue':
        return 'bg-blue-50 text-blue-600 border-blue-200';
      case 'green':
        return 'bg-green-50 text-green-600 border-green-200';
      case 'purple':
        return 'bg-purple-50 text-purple-600 border-purple-200';
      case 'orange':
        return 'bg-orange-50 text-orange-600 border-orange-200';
      default:
        return 'bg-gray-50 text-gray-600 border-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
        <button
          onClick={loadDashboardStats}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          Refresh Data
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card) => (
          <div key={card.title} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">{card.title}</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {formatNumber(card.value)}
                </p>
                <p className="text-sm text-gray-500 mt-1">{card.change}</p>
              </div>
              <div className={`w-12 h-12 rounded-lg border flex items-center justify-center ${getCardColorClasses(card.color)}`}>
                <span className="text-2xl">{card.icon}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <button className="w-full text-left p-3 rounded-lg hover:bg-gray-50 border border-gray-200 transition-colors">
              <div className="flex items-center">
                <span className="text-2xl mr-3">👥</span>
                <div>
                  <p className="font-medium text-gray-900">Manage Users</p>
                  <p className="text-sm text-gray-500">View and manage user accounts</p>
                </div>
              </div>
            </button>
            
            <button className="w-full text-left p-3 rounded-lg hover:bg-gray-50 border border-gray-200 transition-colors">
              <div className="flex items-center">
                <span className="text-2xl mr-3">📝</span>
                <div>
                  <p className="font-medium text-gray-900">Content Moderation</p>
                  <p className="text-sm text-gray-500">Review and moderate posts & comments</p>
                </div>
              </div>
            </button>
            
            <button className="w-full text-left p-3 rounded-lg hover:bg-gray-50 border border-gray-200 transition-colors">
              <div className="flex items-center">
                <span className="text-2xl mr-3">📈</span>
                <div>
                  <p className="font-medium text-gray-900">View Analytics</p>
                  <p className="text-sm text-gray-500">Detailed site analytics and reports</p>
                </div>
              </div>
            </button>
          </div>
        </div>

        {/* System Info */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">System Information</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Total Storage Used</span>
              <span className="text-sm font-medium text-gray-900">---</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Database Size</span>
              <span className="text-sm font-medium text-gray-900">---</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Last Backup</span>
              <span className="text-sm font-medium text-gray-900">---</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Server Status</span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Online
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Welcome Message */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg p-6 text-white">
        <h2 className="text-xl font-semibold mb-2">Welcome to the Admin Dashboard</h2>
        <p className="text-indigo-100">
          Manage your BloggingApp from this central dashboard. Monitor user activity, 
          moderate content, and maintain the platform with comprehensive admin tools.
        </p>
        <div className="mt-4">
          <span className="text-sm text-indigo-200">
            📱 Desktop-only access ensures optimal security and functionality
          </span>
        </div>
      </div>
    </div>
  );
}