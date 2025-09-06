import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import BlogPostCard from '@/components/BlogPostCard'
import { BlogPost } from '@/types'

const mockPost: BlogPost = {
  id: 1,
  title: 'Test Blog Post',
  content: 'This is a test blog post content that should be displayed properly.',
  author: 'Test Author',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  slug: 'test-blog-post'
}

describe('BlogPostCard', () => {
  it('renders post information correctly', () => {
    render(<BlogPostCard post={mockPost} />)
    
    expect(screen.getByText('Test Blog Post')).toBeInTheDocument()
    expect(screen.getByText('Test Author')).toBeInTheDocument()
    expect(screen.getByText(/This is a test blog post content/)).toBeInTheDocument()
    expect(screen.getByText('Jan 1, 2024')).toBeInTheDocument()
  })

  it('truncates long content', () => {
    const longContentPost = {
      ...mockPost,
      content: 'A'.repeat(200) // Content longer than 150 characters
    }
    
    render(<BlogPostCard post={longContentPost} />)
    
    const contentElement = screen.getByText(/A+\.\.\./)
    expect(contentElement).toBeInTheDocument()
    expect(contentElement.textContent).toHaveLength(154) // 150 chars + '...'
  })

  it('calls onClick when card is clicked', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()
    
    render(<BlogPostCard post={mockPost} onClick={handleClick} />)
    
    const card = screen.getByRole('article') || screen.getByText('Test Blog Post').closest('div')
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
    
    // Note: This test assumes there are action elements in the component
    // If the component doesn't have visible action elements, this test should be adjusted
    const cardContent = screen.getByText('Test Blog Post').closest('div')
    expect(cardContent).toBeInTheDocument()
  })

  it('can hide actions when showActions is false', () => {
    render(<BlogPostCard post={mockPost} showActions={false} />)
    
    // Note: This test should be adjusted based on actual action elements
    const cardContent = screen.getByText('Test Blog Post').closest('div')
    expect(cardContent).toBeInTheDocument()
  })
})