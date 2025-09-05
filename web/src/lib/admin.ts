import { User, UserRole } from '@/types';

// Admin role checking utilities
export const isAdmin = (user: User | null): boolean => {
  return user?.role === UserRole.ADMIN || user?.role === UserRole.SUPER_ADMIN;
};

export const isSuperAdmin = (user: User | null): boolean => {
  return user?.role === UserRole.SUPER_ADMIN;
};

export const hasAdminAccess = (user: User | null): boolean => {
  return isAdmin(user);
};

// Role display utilities
export const getRoleDisplayName = (role: UserRole): string => {
  switch (role) {
    case UserRole.SUPER_ADMIN:
      return 'Super Admin';
    case UserRole.ADMIN:
      return 'Admin';
    case UserRole.USER:
      return 'User';
    default:
      return 'Unknown';
  }
};

export const getRoleBadgeClass = (role: UserRole): string => {
  switch (role) {
    case UserRole.SUPER_ADMIN:
      return 'bg-purple-100 text-purple-800 border-purple-200';
    case UserRole.ADMIN:
      return 'bg-blue-100 text-blue-800 border-blue-200';
    case UserRole.USER:
      return 'bg-gray-100 text-gray-800 border-gray-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
};

// Device detection utilities
export const isDesktop = (): boolean => {
  if (typeof window === 'undefined') return true; // SSR safe default
  return window.innerWidth >= 1024; // Desktop is 1024px and above
};

export const isMobile = (): boolean => {
  if (typeof window === 'undefined') return false; // SSR safe default
  return window.innerWidth < 1024;
};

export const detectMobileUserAgent = (): boolean => {
  if (typeof navigator === 'undefined') return false; // SSR safe
  
  const userAgent = navigator.userAgent.toLowerCase();
  const mobileKeywords = [
    'mobile', 'android', 'iphone', 'ipad', 'ipod', 
    'blackberry', 'windows phone', 'webos'
  ];
  
  return mobileKeywords.some(keyword => userAgent.includes(keyword));
};

export const shouldBlockMobileAccess = (): boolean => {
  return isMobile() || detectMobileUserAgent();
};

// Admin dashboard navigation items
export interface AdminNavItem {
  id: string;
  label: string;
  path: string;
  icon: string;
  requiredRole?: UserRole;
  badge?: string;
}

export const getAdminNavItems = (user: User | null): AdminNavItem[] => {
  const baseItems: AdminNavItem[] = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      path: '/admin',
      icon: '📊',
    },
    {
      id: 'users',
      label: 'User Management',
      path: '/admin/users',
      icon: '👥',
    },
    {
      id: 'content',
      label: 'Content Moderation',
      path: '/admin/content',
      icon: '📝',
    },
    {
      id: 'analytics',
      label: 'Analytics',
      path: '/admin/analytics',
      icon: '📈',
    },
  ];

  // Add super admin only items
  if (isSuperAdmin(user)) {
    baseItems.push(
      {
        id: 'settings',
        label: 'System Settings',
        path: '/admin/settings',
        icon: '⚙️',
        requiredRole: UserRole.SUPER_ADMIN,
      },
      {
        id: 'logs',
        label: 'Audit Logs',
        path: '/admin/logs',
        icon: '📋',
        requiredRole: UserRole.SUPER_ADMIN,
      }
    );
  }

  return baseItems;
};

// Format utilities for admin display
export const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

export const formatRelativeTime = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
  return `${Math.floor(diffDays / 365)} years ago`;
};