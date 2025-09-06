import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SearchComponent from '@/components/SearchComponent'

// Mock the API module
vi.mock('@/lib/api', () => ({
  searchPosts: vi.fn(),
  getSearchSuggestions: vi.fn(),
  getSearchFilters: vi.fn()
}))

import { searchPosts, getSearchSuggestions, getSearchFilters } from '@/lib/api'

describe('SearchComponent', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders search form correctly', () => {
    render(<SearchComponent />)
    
    expect(screen.getByPlaceholderText(/search posts/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument()
  })

  it('performs search when form is submitted', async () => {
    const mockSearchResults = {
      results: [
        {
          id: 1,
          title: 'Test Post',
          content: 'Test content',
          author_username: 'testuser',
          published: '2024-01-01T00:00:00Z',
          slug: 'test-post'
        }
      ],
      total: 1,
      has_more: false,
      offset: 0
    }

    vi.mocked(searchPosts).mockResolvedValue(mockSearchResults)

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    const searchButton = screen.getByRole('button', { name: /search/i })
    
    await user.type(searchInput, 'test query')
    await user.click(searchButton)
    
    await waitFor(() => {
      expect(searchPosts).toHaveBeenCalledWith('test query', {})
    })

    await waitFor(() => {
      expect(screen.getByText('Test Post')).toBeInTheDocument()
    })
  })

  it('displays loading state during search', async () => {
    vi.mocked(searchPosts).mockImplementation(() => new Promise(resolve => setTimeout(() => resolve({
      results: [],
      total: 0,
      has_more: false,
      offset: 0
    }), 1000)))

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    const searchButton = screen.getByRole('button', { name: /search/i })
    
    await user.type(searchInput, 'test')
    await user.click(searchButton)
    
    expect(screen.getByText(/searching/i)).toBeInTheDocument()
  })

  it('shows suggestions when typing in search input', async () => {
    const mockSuggestions = {
      titles: ['React Tutorial', 'React Hooks'],
      categories: ['Technology'],
      tags: ['react', 'javascript'],
      authors: ['john_doe']
    }

    vi.mocked(getSearchSuggestions).mockResolvedValue(mockSuggestions)

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    
    await user.type(searchInput, 'react')
    
    await waitFor(() => {
      expect(getSearchSuggestions).toHaveBeenCalledWith('react')
    })

    await waitFor(() => {
      expect(screen.getByText('React Tutorial')).toBeInTheDocument()
      expect(screen.getByText('React Hooks')).toBeInTheDocument()
    })
  })

  it('handles search errors gracefully', async () => {
    vi.mocked(searchPosts).mockRejectedValue(new Error('Search failed'))

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    const searchButton = screen.getByRole('button', { name: /search/i })
    
    await user.type(searchInput, 'test')
    await user.click(searchButton)
    
    await waitFor(() => {
      expect(screen.getByText(/error occurred while searching/i)).toBeInTheDocument()
    })
  })

  it('applies filters correctly', async () => {
    const mockSearchResults = {
      results: [],
      total: 0,
      has_more: false,
      offset: 0
    }

    vi.mocked(searchPosts).mockResolvedValue(mockSearchResults)

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    
    // Open filters
    const filtersButton = screen.getByText(/filters/i)
    await user.click(filtersButton)
    
    // Apply category filter (assuming there's a category select)
    const categorySelect = screen.getByRole('combobox', { name: /category/i })
    await user.selectOptions(categorySelect, 'Technology')
    
    await user.type(searchInput, 'test')
    
    const searchButton = screen.getByRole('button', { name: /search/i })
    await user.click(searchButton)
    
    await waitFor(() => {
      expect(searchPosts).toHaveBeenCalledWith('test', { category: 'Technology' })
    })
  })

  it('clears search results when input is cleared', async () => {
    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    
    // Type and clear
    await user.type(searchInput, 'test')
    await user.clear(searchInput)
    
    // Should not show any search results
    expect(screen.queryByText(/results for/i)).not.toBeInTheDocument()
  })
})