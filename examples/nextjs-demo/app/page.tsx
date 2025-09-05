import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Welcome to <span className="text-primary">BloggingApp</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          A modern, full-stack blogging platform featuring Next.js web application 
          and Flutter mobile app, powered by FastAPI backend with JWT authentication.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/blog"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary hover:bg-primary/90 transition-colors"
          >
            Explore Blog Posts
          </Link>
          <Link
            href="/auth/register"
            className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
          >
            Get Started
          </Link>
        </div>
      </div>

      {/* Comparison Section */}
      <div className="bg-white rounded-lg shadow-sm border p-8 mb-16">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          Why Next.js for Web Platform?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <span className="text-2xl">🔍</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">SEO Excellence</h3>
            <p className="text-gray-600">
              Server-side rendering ensures perfect SEO for blog content discovery
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <span className="text-2xl">⚡</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Performance</h3>
            <p className="text-gray-600">
              Fast loading times and excellent Core Web Vitals scores
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <span className="text-2xl">🛠️</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Rich Ecosystem</h3>
            <p className="text-gray-600">
              Extensive React ecosystem perfect for content-driven applications
            </p>
          </div>
        </div>
      </div>

      {/* Technology Comparison */}
      <div className="bg-white rounded-lg shadow-sm border p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          Technology Comparison Summary
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4">Feature</th>
                <th className="text-center py-3 px-4">Flutter Web</th>
                <th className="text-center py-3 px-4">Next.js</th>
                <th className="text-center py-3 px-4">Nuxt.js</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              <tr>
                <td className="py-3 px-4 font-medium">SEO Optimization</td>
                <td className="py-3 px-4 text-center">❌ Poor</td>
                <td className="py-3 px-4 text-center">✅ Excellent</td>
                <td className="py-3 px-4 text-center">✅ Excellent</td>
              </tr>
              <tr>
                <td className="py-3 px-4 font-medium">Code Reuse (Mobile)</td>
                <td className="py-3 px-4 text-center">✅ 90%+</td>
                <td className="py-3 px-4 text-center">❌ 0%</td>
                <td className="py-3 px-4 text-center">❌ 0%</td>
              </tr>
              <tr>
                <td className="py-3 px-4 font-medium">Performance</td>
                <td className="py-3 px-4 text-center">❌ Slow</td>
                <td className="py-3 px-4 text-center">✅ Fast</td>
                <td className="py-3 px-4 text-center">✅ Fast</td>
              </tr>
              <tr>
                <td className="py-3 px-4 font-medium">Content-First Design</td>
                <td className="py-3 px-4 text-center">❌ Not optimized</td>
                <td className="py-3 px-4 text-center">✅ Perfect</td>
                <td className="py-3 px-4 text-center">✅ Excellent</td>
              </tr>
              <tr>
                <td className="py-3 px-4 font-medium">Ecosystem Size</td>
                <td className="py-3 px-4 text-center">⚠️ Medium</td>
                <td className="py-3 px-4 text-center">✅ Large</td>
                <td className="py-3 px-4 text-center">⚠️ Medium</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <p className="text-blue-800 font-medium">
            <strong>Recommendation:</strong> Next.js is the best choice for this blogging platform due to 
            its superior SEO capabilities, performance optimization, and rich ecosystem for content-driven applications.
          </p>
        </div>
      </div>
    </div>
  );
}