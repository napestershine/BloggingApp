import { Metadata } from 'next';
import Link from 'next/link';
import { ArrowRight, BookOpen, Users, Zap } from 'lucide-react';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';

export const metadata: Metadata = {
  title: 'Home',
  description: 'Welcome to BloggingApp - A modern platform for sharing your stories and connecting with readers worldwide.',
};

export default function HomePage() {
  return (
    <>
      <Header />
      <main>
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 to-white py-20 sm:py-32">
          <div className="mx-auto max-w-7xl px-6 lg:px-8">
            <div className="mx-auto max-w-2xl text-center">
              <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                Share Your Stories with the World
              </h1>
              <p className="mt-6 text-lg leading-8 text-gray-600">
                BloggingApp is a modern platform where writers and readers connect. 
                Create beautiful posts, build your audience, and join a community of storytellers.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Link
                  href="/blog"
                  className="rounded-md bg-primary-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
                >
                  Explore Posts
                </Link>
                <Link
                  href="/auth/register"
                  className="text-sm font-semibold leading-6 text-gray-900 flex items-center gap-2 hover:text-primary-600"
                >
                  Start Writing <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-24 sm:py-32">
          <div className="mx-auto max-w-7xl px-6 lg:px-8">
            <div className="mx-auto max-w-2xl lg:text-center">
              <h2 className="text-base font-semibold leading-7 text-primary-600">
                Why BloggingApp?
              </h2>
              <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Everything you need to share your voice
              </p>
              <p className="mt-6 text-lg leading-8 text-gray-600">
                Our platform combines the best of modern web technology with a focus on 
                great writing and meaningful connections.
              </p>
            </div>
            <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
              <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
                <div className="relative pl-16">
                  <dt className="text-base font-semibold leading-7 text-gray-900">
                    <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600">
                      <BookOpen className="h-6 w-6 text-white" />
                    </div>
                    Beautiful Writing Experience
                  </dt>
                  <dd className="mt-2 text-base leading-7 text-gray-600">
                    Focus on your content with our clean, distraction-free editor. 
                    Rich text formatting and markdown support included.
                  </dd>
                </div>
                <div className="relative pl-16">
                  <dt className="text-base font-semibold leading-7 text-gray-900">
                    <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600">
                      <Users className="h-6 w-6 text-white" />
                    </div>
                    Engaged Community
                  </dt>
                  <dd className="mt-2 text-base leading-7 text-gray-600">
                    Connect with readers through comments and discussions. 
                    Build your following and discover new voices.
                  </dd>
                </div>
                <div className="relative pl-16">
                  <dt className="text-base font-semibold leading-7 text-gray-900">
                    <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600">
                      <Zap className="h-6 w-6 text-white" />
                    </div>
                    Fast & Reliable
                  </dt>
                  <dd className="mt-2 text-base leading-7 text-gray-600">
                    Built with modern technology for lightning-fast load times 
                    and excellent SEO performance.
                  </dd>
                </div>
                <div className="relative pl-16">
                  <dt className="text-base font-semibold leading-7 text-gray-900">
                    <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600">
                      <BookOpen className="h-6 w-6 text-white" />
                    </div>
                    Mobile-First Design
                  </dt>
                  <dd className="mt-2 text-base leading-7 text-gray-600">
                    Read and write seamlessly across all devices. 
                    Responsive design ensures great experience everywhere.
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative isolate overflow-hidden bg-gray-900 py-24 sm:py-32">
          <div className="mx-auto max-w-7xl px-6 lg:px-8">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                Ready to Start Writing?
              </h2>
              <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-300">
                Join thousands of writers who are already sharing their stories on BloggingApp. 
                It's free to get started.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Link
                  href="/auth/register"
                  className="rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
                >
                  Create Account
                </Link>
                <Link
                  href="/blog"
                  className="text-sm font-semibold leading-6 text-white"
                >
                  Browse Posts <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}