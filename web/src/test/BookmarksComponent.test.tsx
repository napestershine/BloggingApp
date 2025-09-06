import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import BookmarksComponent from '@/components/BookmarksComponent'

// Mock the API module
vi.mock('@/lib/api', () => ({
  getUserBookmarks: vi.fn(),
  removeBookmark: vi.fn()
}))

import { getUserBookmarks, removeBookmark } from '@/lib/api'

describe('BookmarksComponent', () => {
  const mockUserId = 1

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders bookmarks list correctly', async () => {
    const mockBookmarks = {
      bookmarks: [
        {
          id: 1,
          user_id: 1,
          post_id: 1,
          created_at: '2024-01-01T00:00:00Z',
          post: {
            id: 1,
            title: 'How to Learn React',
            content: 'A comprehensive guide to learning React',
            author_username: 'john_doe',
            published: '2024-01-01T00:00:00Z',
            slug: 'how-to-learn-react'
          }
        }
      ],
      total: 1,
      has_more: false,
      offset: 0
    }

    vi.mocked(getUserBookmarks).mockResolvedValue(mockBookmarks)

    render(<BookmarksComponent userId={mockUserId} />)

    await waitFor(() => {
      expect(getUserBookmarks).toHaveBeenCalledWith(mockUserId, 0, 10)
    })

    await waitFor(() => {
      expect(screen.getByText('How to Learn React')).toBeInTheDocument()
      expect(screen.getByText(/by john_doe/i)).toBeInTheDocument()
    })
  })

  it('shows empty state when no bookmarks', async () => {
    const mockEmptyBookmarks = {
      bookmarks: [],
      total: 0,
      has_more: false,
      offset: 0
    }

    vi.mocked(getUserBookmarks).mockResolvedValue(mockEmptyBookmarks)

    render(<BookmarksComponent userId={mockUserId} />)

    await waitFor(() => {
      expect(screen.getByText(/no bookmarks yet/i)).toBeInTheDocument()
    })
  })

  it('displays loading state initially', () => {
    vi.mocked(getUserBookmarks).mockImplementation(() => new Promise(() => {})) // Never resolves

    render(<BookmarksComponent userId={mockUserId} />)

    expect(screen.getByText(/loading bookmarks/i)).toBeInTheDocument()
  })

  it('handles remove bookmark correctly', async () => {
    const mockBookmarks = {
      bookmarks: [
        {
          id: 1,
          user_id: 1,
          post_id: 1,
          created_at: '2024-01-01T00:00:00Z',
          post: {
            id: 1,
            title: 'How to Learn React',
            content: 'A comprehensive guide to learning React',
            author_username: 'john_doe',
            published: '2024-01-01T00:00:00Z',
            slug: 'how-to-learn-react'
          }
        }
      ],
      total: 1,
      has_more: false,
      offset: 0
    }

    vi.mocked(getUserBookmarks).mockResolvedValue(mockBookmarks)
    vi.mocked(removeBookmark).mockResolvedValue({ message: 'Bookmark removed successfully' })

    const user = userEvent.setup()
    render(<BookmarksComponent userId={mockUserId} />)

    await waitFor(() => {
      expect(screen.getByText('How to Learn React')).toBeInTheDocument()
    })

    // Find and click remove button
    const removeButton = screen.getByRole('button', { name: /remove/i })
    await user.click(removeButton)

    // Confirm deletion in dialog
    const confirmButton = screen.getByRole('button', { name: /confirm/i })
    await user.click(confirmButton)

    await waitFor(() => {
      expect(removeBookmark).toHaveBeenCalledWith(1, 1)
    })
  })

  it('loads more bookmarks when load more button is clicked', async () => {
    const mockBookmarksPage1 = {
      bookmarks: [
        {
          id: 1,
          user_id: 1,
          post_id: 1,
          created_at: '2024-01-01T00:00:00Z',
          post: {
            id: 1,
            title: 'First Post',
            content: 'Content 1',
            author_username: 'author1',
            published: '2024-01-01T00:00:00Z',
            slug: 'first-post'
          }
        }
      ],
      total: 2,
      has_more: true,
      offset: 0
    }

    const mockBookmarksPage2 = {
      bookmarks: [
        {
          id: 2,
          user_id: 1,
          post_id: 2,
          created_at: '2024-01-02T00:00:00Z',
          post: {
            id: 2,
            title: 'Second Post',
            content: 'Content 2',
            author_username: 'author2',
            published: '2024-01-02T00:00:00Z',
            slug: 'second-post'
          }
        }
      ],
      total: 2,
      has_more: false,
      offset: 1
    }

    vi.mocked(getUserBookmarks)
      .mockResolvedValueOnce(mockBookmarksPage1)
      .mockResolvedValueOnce(mockBookmarksPage2)

    const user = userEvent.setup()
    render(<BookmarksComponent userId={mockUserId} />)

    await waitFor(() => {
      expect(screen.getByText('First Post')).toBeInTheDocument()
    })

    // Click load more button
    const loadMoreButton = screen.getByRole('button', { name: /load more/i })
    await user.click(loadMoreButton)

    await waitFor(() => {
      expect(getUserBookmarks).toHaveBeenCalledWith(mockUserId, 1, 10)
    })

    await waitFor(() => {
      expect(screen.getByText('Second Post')).toBeInTheDocument()
    })
  })

  it('handles API errors gracefully', async () => {
    vi.mocked(getUserBookmarks).mockRejectedValue(new Error('Failed to fetch bookmarks'))

    render(<BookmarksComponent userId={mockUserId} />)

    await waitFor(() => {
      expect(screen.getByText(/error loading bookmarks/i)).toBeInTheDocument()
    })
  })

  it('shows bookmark date correctly', async () => {
    const mockBookmarks = {
      bookmarks: [
        {
          id: 1,
          user_id: 1,
          post_id: 1,
          created_at: '2024-01-15T10:30:00Z',
          post: {
            id: 1,
            title: 'Test Post',
            content: 'Test content',
            author_username: 'testuser',
            published: '2024-01-01T00:00:00Z',
            slug: 'test-post'
          }
        }
      ],
      total: 1,
      has_more: false,
      offset: 0
    }

    vi.mocked(getUserBookmarks).mockResolvedValue(mockBookmarks)

    render(<BookmarksComponent userId={mockUserId} />)

    await waitFor(() => {
      expect(screen.getByText(/bookmarked on/i)).toBeInTheDocument()
    })
  })
})