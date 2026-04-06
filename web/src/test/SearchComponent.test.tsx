// @ts-nocheck - Test file with interface mismatches
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SearchComponent from '@/components/SearchComponent'

const searchApiMocks = vi.hoisted(() => ({
  searchAPI: {
    searchPosts: vi.fn(),
    getSuggestions: vi.fn(),
    getFilters: vi.fn(),
  },
}))

vi.mock('@/lib/api', () => ({
  ...searchApiMocks,
}))

describe('SearchComponent', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    searchApiMocks.searchAPI.getFilters.mockResolvedValue({
      categories: [{ name: 'Technology', slug: 'technology' }],
      tags: [{ name: 'react', post_count: 5 }],
      authors: [{ username: 'john_doe', post_count: 3 }],
    })
  })

  it('renders search form correctly', () => {
    render(<SearchComponent />)
    
    expect(screen.getByPlaceholderText(/search posts/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /^search$/i })).toBeInTheDocument()
  })

  it('performs search when form is submitted', async () => {
    const mockSearchResults = [
      {
        id: 1,
        title: 'Test Post',
        content: 'Test content',
        author_username: 'testuser',
        published: '2024-01-01T00:00:00Z',
        slug: 'test-post'
      }
    ]

    searchApiMocks.searchAPI.searchPosts.mockResolvedValue(mockSearchResults)

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    const searchButton = screen.getByRole('button', { name: /^search$/i })
    
    await user.type(searchInput, 'test query')
    await user.click(searchButton)
    
    await waitFor(() => {
      expect(searchApiMocks.searchAPI.searchPosts).toHaveBeenCalledWith(
        expect.objectContaining({ q: 'test query' })
      )
    })

    await waitFor(() => {
      expect(screen.getByText('Test Post')).toBeInTheDocument()
    })
  })

  it('displays loading state during search', async () => {
    searchApiMocks.searchAPI.searchPosts.mockImplementation(() => new Promise(() => {}))

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    const searchButton = screen.getByRole('button', { name: /^search$/i })
    
    await user.type(searchInput, 'test')
    await user.click(searchButton)
    
    expect(screen.getByText(/searching/i)).toBeInTheDocument()
  })

  it('shows suggestions when typing in search input', async () => {
    const mockSuggestions = [
      { text: 'React Tutorial', type: 'title', description: 'Matching title' },
      { text: 'React Hooks', type: 'title', description: 'Matching title' },
    ]

    searchApiMocks.searchAPI.getSuggestions.mockResolvedValue(mockSuggestions)

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    
    await user.type(searchInput, 'react')
    
    await waitFor(() => {
      expect(searchApiMocks.searchAPI.getSuggestions).toHaveBeenCalledWith('react')
    })

    await waitFor(() => {
      expect(screen.getByText('React Tutorial')).toBeInTheDocument()
      expect(screen.getByText('React Hooks')).toBeInTheDocument()
    })
  })

  it('handles search errors gracefully', async () => {
    searchApiMocks.searchAPI.searchPosts.mockRejectedValue(new Error('Search failed'))

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    const searchButton = screen.getByRole('button', { name: /^search$/i })
    
    await user.type(searchInput, 'test')
    await user.click(searchButton)
    
    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/error occurred while searching/i)
    })
  })

  it('applies filters correctly', async () => {
    searchApiMocks.searchAPI.searchPosts.mockResolvedValue([])

    const user = userEvent.setup()
    render(<SearchComponent />)
    
    const searchInput = screen.getByPlaceholderText(/search posts/i)
    const categorySelect = await screen.findByRole('combobox', { name: /category/i })
    await user.selectOptions(categorySelect, 'Technology')
    
    await user.type(searchInput, 'test')
    
    const searchButton = screen.getByRole('button', { name: /^search$/i })
    await user.click(searchButton)
    
    await waitFor(() => {
      expect(searchApiMocks.searchAPI.searchPosts).toHaveBeenCalledWith(
        expect.objectContaining({ q: 'test', category: 'Technology' })
      )
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
