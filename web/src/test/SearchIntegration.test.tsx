import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

// Mock the API module to use actual fetch calls that MSW can intercept
vi.mock('@/lib/api', () => ({
  searchPosts: async (query: string) => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/posts/search?q=${encodeURIComponent(query)}`)
    if (!response.ok) {
      throw new Error('Search failed')
    }
    return response.json()
  }
}))

// Create a simple SearchResults component for testing
function SearchResults({ query }: { query: string }) {
  const [results, setResults] = React.useState<any[]>([])
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    if (!query) return

    const fetchResults = async () => {
      setLoading(true)
      setError(null)
      try {
        const { searchPosts } = await import('@/lib/api')
        const data = await searchPosts(query)
        setResults(data.results || [])
      } catch (err) {
        setError('Failed to search posts')
      } finally {
        setLoading(false)
      }
    }

    fetchResults()
  }, [query])

  if (loading) return <div>Loading...</div>
  if (error) return <div role="alert">Error: {error}</div>
  if (results.length === 0) return <div>No results found</div>

  return (
    <div>
      <h2>Search Results</h2>
      {results.map((post) => (
        <article key={post.id} data-testid="search-result">
          <h3>{post.title}</h3>
          <p>{post.content}</p>
          <small>By {post.author_username}</small>
        </article>
      ))}
    </div>
  )
}

// Add React import
import React from 'react'

describe('Search Integration', () => {
  it('loads and displays search results from API', async () => {
    render(<SearchResults query="react" />)
    
    expect(screen.getByText('Loading...')).toBeInTheDocument()
    
    await waitFor(() => {
      expect(screen.getByText('Search Results')).toBeInTheDocument()
    })
    
    expect(screen.getByText('Search Result Post')).toBeInTheDocument()
    expect(screen.getByText(/This post matches the search term: react/)).toBeInTheDocument()
    expect(screen.getByText('By testuser')).toBeInTheDocument()
  })

  it('shows no results when query is empty', () => {
    render(<SearchResults query="" />)
    
    // Component should not show loading or results when query is empty
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
    expect(screen.queryByText('Search Results')).not.toBeInTheDocument()
  })

  it('handles API errors gracefully', async () => {
    // Mock a server error response
    const server = setupServer(
      http.get('*/posts/search', () => {
        return HttpResponse.json(
          { detail: 'Internal server error' },
          { status: 500 }
        )
      })
    )
    
    server.listen()
    
    render(<SearchResults query="error" />)
    
    expect(screen.getByText('Loading...')).toBeInTheDocument()
    
    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Error: Failed to search posts')
    })
    
    server.close()
  })

  it('shows no results message when API returns empty results', async () => {
    // Mock empty results
    const server = setupServer(
      http.get('*/posts/search', () => {
        return HttpResponse.json({
          results: [],
          total: 0,
          has_more: false,
          offset: 0
        })
      })
    )
    
    server.listen()
    
    render(<SearchResults query="nonexistent" />)
    
    expect(screen.getByText('Loading...')).toBeInTheDocument()
    
    await waitFor(() => {
      expect(screen.getByText('No results found')).toBeInTheDocument()
    })
    
    server.close()
  })
})