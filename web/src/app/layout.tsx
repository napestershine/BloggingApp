import '@/styles/globals.css';
import { Inter } from 'next/font/google';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from '@/components/AuthProvider';
import { ThemeProvider } from '@/components/ThemeProvider';
import { Metadata } from 'next';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    template: '%s | BloggingApp',
    default: 'BloggingApp - Share Your Stories',
  },
  description: 'A modern blogging platform built with Next.js and FastAPI',
  keywords: ['blog', 'writing', 'stories', 'articles', 'nextjs', 'fastapi'],
  authors: [{ name: 'BloggingApp Team' }],
  creator: 'BloggingApp',
  publisher: 'BloggingApp',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000',
    siteName: 'BloggingApp',
    title: 'BloggingApp - Share Your Stories',
    description: 'A modern blogging platform built with Next.js and FastAPI',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BloggingApp - Share Your Stories',
    description: 'A modern blogging platform built with Next.js and FastAPI',
    creator: '@bloggingapp',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>
          <AuthProvider>
            {children}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: 'var(--toast-bg, #363636)',
                  color: 'var(--toast-color, #fff)',
                  borderRadius: '8px',
                },
                success: {
                  duration: 3000,
                  iconTheme: {
                    primary: 'var(--success-color, #4ade80)',
                    secondary: 'var(--success-text, #fff)',
                  },
                },
                error: {
                  duration: 5000,
                  iconTheme: {
                    primary: 'var(--error-color, #ef4444)',
                    secondary: 'var(--error-text, #fff)',
                  },
                },
              }}
            />
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}