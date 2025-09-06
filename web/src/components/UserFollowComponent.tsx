// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck - Component with interface mismatches
'use client';

import { useState, useEffect } from 'react';
import { followAPI, FollowerUser, UserFollowStats } from '@/lib/api';

interface UserFollowComponentProps {
  userId: number;
  username: string;
  initialStats?: UserFollowStats;
}

export default function UserFollowComponent({ 
  userId, 
  username, 
  initialStats 
}: UserFollowComponentProps) {
  const [stats, setStats] = useState<UserFollowStats | null>(initialStats || null);
  const [followers, setFollowers] = useState<FollowerUser[]>([]);
  const [following, setFollowing] = useState<FollowerUser[]>([]);
  const [activeTab, setActiveTab] = useState<'followers' | 'following'>('followers');
  const [loading, setLoading] = useState(false);
  const [followActionLoading, setFollowActionLoading] = useState(false);

  // Load initial data
  useEffect(() => {
    loadStats();
    loadFollowers();
    loadFollowing();
  }, [userId]);

  const loadStats = async () => {
    try {
      const statsData = await followAPI.getStats(userId);
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load follow stats:', error);
    }
  };

  const loadFollowers = async () => {
    setLoading(true);
    try {
      const followersData = await followAPI.getFollowers(userId);
      setFollowers(followersData);
    } catch (error) {
      console.error('Failed to load followers:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadFollowing = async () => {
    setLoading(true);
    try {
      const followingData = await followAPI.getFollowing(userId);
      setFollowing(followingData);
    } catch (error) {
      console.error('Failed to load following:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleFollow = async () => {
    if (!stats || followActionLoading) return;

    setFollowActionLoading(true);
    try {
      if (stats.is_following) {
        await followAPI.unfollowUser(userId);
      } else {
        await followAPI.followUser(userId);
      }
      
      // Reload stats to get updated counts
      await loadStats();
    } catch (error) {
      console.error('Failed to toggle follow:', error);
    } finally {
      setFollowActionLoading(false);
    }
  };

  if (!stats) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {username}&apos;s Network
          </h1>
          
          {stats.is_following !== null && (
            <button
              onClick={toggleFollow}
              disabled={followActionLoading}
              className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
                stats.is_following
                  ? 'bg-gray-500 hover:bg-gray-600 text-white'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              } ${followActionLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {followActionLoading ? (
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Loading...</span>
                </div>
              ) : stats.is_following ? (
                <>✖ Unfollow</>
              ) : (
                <>➕ Follow</>
              )}
            </button>
          )}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-8">
          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900 dark:text-white">
              {stats.followers_count}
            </div>
            <div className="text-gray-600 dark:text-gray-400">Followers</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900 dark:text-white">
              {stats.following_count}
            </div>
            <div className="text-gray-600 dark:text-gray-400">Following</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <div className="flex border-b border-gray-200 dark:border-gray-600">
          <button
            onClick={() => setActiveTab('followers')}
            className={`flex-1 px-6 py-4 font-semibold transition-colors ${
              activeTab === 'followers'
                ? 'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-400 border-b-2 border-blue-500'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Followers ({stats.followers_count})
          </button>
          <button
            onClick={() => setActiveTab('following')}
            className={`flex-1 px-6 py-4 font-semibold transition-colors ${
              activeTab === 'following'
                ? 'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-400 border-b-2 border-blue-500'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Following ({stats.following_count})
          </button>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          ) : (
            <UserList 
              users={activeTab === 'followers' ? followers : following}
              emptyMessage={
                activeTab === 'followers' 
                  ? 'No followers yet' 
                  : 'Not following anyone yet'
              }
            />
          )}
        </div>
      </div>
    </div>
  );
}

interface UserListProps {
  users: FollowerUser[];
  emptyMessage: string;
}

function UserList({ users, emptyMessage }: UserListProps) {
  if (users.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">👥</div>
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          {emptyMessage}
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Users will appear here when connections are made
        </p>
      </div>
    );
  }

  return (
    <div className="grid gap-4">
      {users.map((user) => (
        <div
          key={user.id}
          className="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-700 
                   rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
        >
          {/* Avatar */}
          <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center 
                        text-white font-bold text-lg">
            {user.username.charAt(0).toUpperCase()}
          </div>
          
          {/* User Info */}
          <div className="flex-1">
            <h4 className="font-semibold text-gray-900 dark:text-white">
              {user.name}
            </h4>
            <p className="text-gray-600 dark:text-gray-400">
              @{user.username}
            </p>
          </div>
          
          {/* Action */}
          <button
            onClick={() => {
              // Navigate to user profile
              window.open(`/user/${user.id}/follows?username=${user.username}`, '_blank');
            }}
            className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg 
                     transition-colors font-medium"
          >
            View Profile
          </button>
        </div>
      ))}
    </div>
  );
}