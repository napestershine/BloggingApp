import { describe, it, expect } from 'vitest'

// Test API functionality with MSW
describe('API with MSW', () => {
  it('should fetch posts from mocked API', async () => {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    
    const response = await fetch(`${API_BASE_URL}/posts`)
    const data = await response.json()
    
    expect(response.ok).toBe(true)
    expect(data.posts).toHaveLength(2)
    expect(data.posts[0].title).toBe('First Blog Post')
    expect(data.posts[1].title).toBe('Second Blog Post')
  })

  it('should handle search API', async () => {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    
    const response = await fetch(`${API_BASE_URL}/posts/search?q=react`)
    const data = await response.json()
    
    console.log('Search response:', data) // Debug log
    
    expect(response.ok).toBe(true)
    expect(data.results).toBeDefined()
    expect(Array.isArray(data.results)).toBe(true)
    expect(data.results).toHaveLength(1)
    expect(data.results[0].title).toBe('Search Result Post')
  })

  it('should handle empty search', async () => {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    
    const response = await fetch(`${API_BASE_URL}/posts/search`)
    const data = await response.json()
    
    console.log('Empty search response:', data) // Debug log
    
    expect(response.ok).toBe(true)
    expect(data.results).toBeDefined()
    expect(Array.isArray(data.results)).toBe(true)
    expect(data.results).toHaveLength(0)
  })
})