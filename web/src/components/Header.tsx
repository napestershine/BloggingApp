'use client';

import Link from 'next/link';
import { useAuth } from './AuthProvider';
import { ThemeToggleButton } from './ThemeToggleButton';
import { BookOpen, LogOut, User, PenTool, Search, Bookmark, Bell } from 'lucide-react';

/**
 * Header component provides the main navigation and branding for the BloggingApp.
 * 
 * This component includes:
 * - Brand logo and site title
 * - Main navigation menu with contextual links
 * - User authentication controls
 * - Theme toggle functionality
 * - Responsive design for mobile and desktop
 * 
 * Features:
 * - Dynamic navigation based on authentication status
 * - Dark/light theme toggle integration
 * - Mobile-responsive navigation (expandable on smaller screens)
 * - User profile access and logout functionality
 * - Clean, accessible design with proper ARIA labels
 * 
 * The header adapts its content based on user authentication:
 * - Unauthenticated: Shows login/register links
 * - Authenticated: Shows user menu, dashboard, and write links
 */
export function Header() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <Link 
            href="/" 
            className="flex items-center space-x-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors duration-200"
          >
            <BookOpen className="h-8 w-8" />
            <span className="text-xl font-bold">BloggingApp</span>
          </Link>

          {/* Main Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link 
              href="/blog" 
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium transition-colors duration-200"
            >
              Blog
            </Link>
            
            <Link 
              href="/search" 
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium flex items-center gap-1 transition-colors duration-200"
            >
              <Search className="h-4 w-4" />
              Search
            </Link>
            
            {isAuthenticated && (
              <>
                <Link 
                  href="/bookmarks" 
                  className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium flex items-center gap-1 transition-colors duration-200"
                >
                  <Bookmark className="h-4 w-4" />
                  Bookmarks
                </Link>
                
                <Link 
                  href="/notifications" 
                  className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium flex items-center gap-1 transition-colors duration-200"
                >
                  <Bell className="h-4 w-4" />
                  Notifications
                </Link>
                
                <Link 
                  href="/write" 
                  className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium flex items-center gap-1 transition-colors duration-200"
                >
                  <PenTool className="h-4 w-4" />
                  Write
                </Link>
                
                <Link 
                  href="/dashboard" 
                  className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium transition-colors duration-200"
                >
                  Dashboard
                </Link>
              </>
            )}
          </nav>

          {/* User Actions and Theme Toggle */}
          <div className="flex items-center space-x-4">
            {/* Theme Toggle Button */}
            <ThemeToggleButton />
            
            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <Link
                  href="/profile"
                  className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors duration-200"
                >
                  <User className="h-5 w-5" />
                  <span className="hidden sm:block">{user?.username}</span>
                </Link>
                <button
                  onClick={logout}
                  className="flex items-center space-x-1 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors duration-200"
                  aria-label="Logout"
                >
                  <LogOut className="h-5 w-5" />
                  <span className="hidden sm:block">Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  href="/auth/login"
                  className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium transition-colors duration-200"
                >
                  Login
                </Link>
                <Link
                  href="/auth/register"
                  className="bg-blue-600 dark:bg-blue-500 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors duration-200"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}