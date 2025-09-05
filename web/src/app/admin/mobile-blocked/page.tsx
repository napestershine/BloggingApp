'use client';

import { useEffect } from 'react';

export default function MobileBlockedPage() {
  useEffect(() => {
    // Prevent back navigation to admin routes on mobile
    window.history.pushState(null, '', window.location.href);
    window.addEventListener('popstate', () => {
      window.history.pushState(null, '', window.location.href);
    });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6 text-center">
        <div className="mb-6">
          <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg 
              className="w-10 h-10 text-orange-600" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" 
              />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Desktop Access Required
          </h1>
          <div className="text-4xl mb-4">🖥️</div>
        </div>
        
        <div className="space-y-4 mb-6">
          <p className="text-gray-600">
            The admin dashboard is designed for desktop use only and is not available on mobile devices.
          </p>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h2 className="text-sm font-semibold text-blue-900 mb-2">
              To access the admin dashboard:
            </h2>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Use a desktop or laptop computer</li>
              <li>• Ensure your screen width is at least 1024px</li>
              <li>• Open this page in a desktop browser</li>
            </ul>
          </div>
        </div>
        
        <div className="space-y-3">
          <button
            onClick={() => window.location.href = '/'}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            Return to Homepage
          </button>
          
          <button
            onClick={() => window.location.reload()}
            className="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors"
          >
            Check Again
          </button>
        </div>
        
        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            This restriction ensures optimal admin experience and security.
          </p>
        </div>
      </div>
    </div>
  );
}