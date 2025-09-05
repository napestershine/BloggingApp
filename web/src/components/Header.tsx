'use client';

import Link from 'next/link';
import { useAuth } from './AuthProvider';
import { BookOpen, LogOut, User, PenTool } from 'lucide-react';

export function Header() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link 
            href="/" 
            className="flex items-center space-x-2 text-primary-600 hover:text-primary-700"
          >
            <BookOpen className="h-8 w-8" />
            <span className="text-xl font-bold">BloggingApp</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link 
              href="/blog" 
              className="text-gray-600 hover:text-gray-900 font-medium"
            >
              Blog
            </Link>
            {isAuthenticated && (
              <>
                <Link 
                  href="/write" 
                  className="text-gray-600 hover:text-gray-900 font-medium flex items-center gap-1"
                >
                  <PenTool className="h-4 w-4" />
                  Write
                </Link>
                <Link 
                  href="/dashboard" 
                  className="text-gray-600 hover:text-gray-900 font-medium"
                >
                  Dashboard
                </Link>
              </>
            )}
          </nav>

          {/* User Actions */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <Link
                  href="/profile"
                  className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
                >
                  <User className="h-5 w-5" />
                  <span className="hidden sm:block">{user?.username}</span>
                </Link>
                <button
                  onClick={logout}
                  className="flex items-center space-x-1 text-gray-600 hover:text-gray-900"
                >
                  <LogOut className="h-5 w-5" />
                  <span className="hidden sm:block">Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  href="/auth/login"
                  className="text-gray-600 hover:text-gray-900 font-medium"
                >
                  Login
                </Link>
                <Link
                  href="/auth/register"
                  className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700 transition-colors"
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