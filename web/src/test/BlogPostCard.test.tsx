import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import BlogPostCard from '@/components/BlogPostCard'
import { BlogPost } from '@/types'

const mockPost: BlogPost = {
  id: 1,
  title: 'Test Blog Post',
  content: 'This is a test blog post content that should be displayed properly in the card component.',
  author: 'Test Author',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  slug: 'test-blog-post'
}

describe('BlogPostCard', () => {
  it('renders post information correctly', () => {
    render(<BlogPostCard post={mockPost} />)
    
    expect(screen.getByText('Test Blog Post')).toBeInTheDocument()
    // Check for author text with emojis - needs to be more flexible
    expect(screen.getByText(/Test Author/)).toBeInTheDocument()
    expect(screen.getByText(/This is a test blog post content/)).toBeInTheDocument()
    expect(screen.getByText(/Jan 1, 2024/)).toBeInTheDocument()
  })

  it('displays the slug when present', () => {
    render(<BlogPostCard post={mockPost} />)
    
    expect(screen.getByText('test-blog-post')).toBeInTheDocument()
  })

  it('truncates long content', () => {
    const longContentPost = {
      ...mockPost,
      content: 'A'.repeat(200) // Content longer than 150 characters
    }
    
    render(<BlogPostCard post={longContentPost} />)
    
    const contentElement = screen.getByText(/A+\.\.\./) // Use regular dots
    expect(contentElement).toBeInTheDocument()
    expect(contentElement.textContent!.length).toBeLessThanOrEqual(154) // Allow for slight variation
  })

  it('does not truncate short content', () => {
    const shortContentPost = {
      ...mockPost,
      content: 'Short content'
    }
    
    render(<BlogPostCard post={shortContentPost} />)
    
    expect(screen.getByText('Short content')).toBeInTheDocument()
    expect(screen.queryByText(/\.\.\.$/)).not.toBeInTheDocument()
  })

  it('calls onClick when card is clicked', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()
    
    render(<BlogPostCard post={mockPost} onClick={handleClick} />)
    
    const card = screen.getByText('Test Blog Post').closest('div')
    await user.click(card!)
    
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('applies cursor-pointer class when onClick is provided', () => {
    const handleClick = vi.fn()
    const { container } = render(<BlogPostCard post={mockPost} onClick={handleClick} />)
    
    const cardElement = container.firstChild as HTMLElement
    expect(cardElement).toHaveClass('cursor-pointer')
  })

  it('does not apply cursor-pointer class when onClick is not provided', () => {
    const { container } = render(<BlogPostCard post={mockPost} />)
    
    const cardElement = container.firstChild as HTMLElement
    expect(cardElement).not.toHaveClass('cursor-pointer')
  })

  it('shows actions by default', () => {
    render(<BlogPostCard post={mockPost} />)
    
    // Look for elements that are only shown when actions are enabled
    expect(screen.getByText('test-blog-post')).toBeInTheDocument() // slug badge
    expect(screen.getByRole('button', { name: '🔗' })).toBeInTheDocument() // share button
    expect(screen.getByRole('button', { name: '🔖' })).toBeInTheDocument() // bookmark button
  })

  it('hides actions when showActions is false', () => {
    render(<BlogPostCard post={mockPost} showActions={false} />)
    
    // The slug badge and action buttons should not be present when actions are hidden
    expect(screen.queryByText('test-blog-post')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: '🔗' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: '🔖' })).not.toBeInTheDocument()
  })

  it('handles post without slug gracefully', () => {
    const postWithoutSlug = {
      ...mockPost,
      slug: undefined
    }
    
    render(<BlogPostCard post={postWithoutSlug} />)
    
    expect(screen.getByText('Test Blog Post')).toBeInTheDocument()
    expect(screen.getByText(/Test Author/)).toBeInTheDocument()
    // Should still show action buttons but no slug badge
    expect(screen.getByRole('button', { name: '🔗' })).toBeInTheDocument()
  })

  it('prevents event propagation on action buttons', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()
    
    render(<BlogPostCard post={mockPost} onClick={handleClick} />)
    
    // Find share button by its emoji and click it
    const shareButton = screen.getByRole('button', { name: '🔗' })
    await user.click(shareButton)
    
    // onClick should not be called because event propagation was stopped
    expect(handleClick).not.toHaveBeenCalled()
  })
})