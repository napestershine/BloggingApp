import Link from 'next/link';
import { BookOpen, Twitter, Github, Mail } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link href="/" className="flex items-center space-x-2 mb-4">
              <BookOpen className="h-8 w-8 text-primary-500" />
              <span className="text-xl font-bold">BloggingApp</span>
            </Link>
            <p className="text-gray-400 max-w-md">
              A modern platform for writers and readers to connect, share stories, 
              and build communities around great content.
            </p>
            <div className="flex space-x-4 mt-6">
              <a href="#" className="text-gray-400 hover:text-white">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white">
                <Github className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white">
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-sm font-semibold text-gray-300 tracking-wider uppercase mb-4">
              Platform
            </h3>
            <ul className="space-y-3">
              <li>
                <Link href="/blog" className="text-gray-400 hover:text-white">
                  Browse Posts
                </Link>
              </li>
              <li>
                <Link href="/write" className="text-gray-400 hover:text-white">
                  Start Writing
                </Link>
              </li>
              <li>
                <Link href="/authors" className="text-gray-400 hover:text-white">
                  Authors
                </Link>
              </li>
              <li>
                <Link href="/topics" className="text-gray-400 hover:text-white">
                  Topics
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-sm font-semibold text-gray-300 tracking-wider uppercase mb-4">
              Support
            </h3>
            <ul className="space-y-3">
              <li>
                <Link href="/help" className="text-gray-400 hover:text-white">
                  Help Center
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-gray-400 hover:text-white">
                  Contact Us
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-gray-400 hover:text-white">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-gray-400 hover:text-white">
                  Terms of Service
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8">
          <p className="text-gray-400 text-center">
            © 2024 BloggingApp. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}