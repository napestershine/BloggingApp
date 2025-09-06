/* eslint-disable @typescript-eslint/no-require-imports */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

// Mock the api module's getApiBaseUrl function
const mockGetApiBaseUrl = vi.fn()

// Mock the api module
vi.mock('@/lib/api', async () => {
  const actual = await vi.importActual('@/lib/api')
  return {
    ...actual,
    getApiBaseUrl: mockGetApiBaseUrl
  }
})

describe('API Base URL Resolution', () => {
  // Store original process.env values
  let originalEnv: typeof process.env

  beforeEach(() => {
    originalEnv = { ...process.env }
    vi.clearAllMocks()
  })

  afterEach(() => {
    process.env = originalEnv
  })

  it('should use NEXT_PUBLIC_API_BASE_URL in browser context', () => {
    // Mock browser environment
    Object.defineProperty(window, 'window', {
      value: {},
      writable: true
    })
    
    process.env.NEXT_PUBLIC_API_BASE_URL = 'https://api.example.com'
    process.env.API_INTERNAL_URL = 'http://api:8000'

    // Import the function after setting up mocks
    const { getApiBaseUrl } = require('@/lib/api')
    
    const result = getApiBaseUrl()
    expect(result).toBe('https://api.example.com')
  })

  it('should use API_INTERNAL_URL in server context', () => {
    // Mock server environment (no window object)
    delete (global as any).window
    
    process.env.NEXT_PUBLIC_API_BASE_URL = 'https://api.example.com'
    process.env.API_INTERNAL_URL = 'http://api:8000'

    // Import the function after setting up mocks
    const { getApiBaseUrl } = require('@/lib/api')
    
    const result = getApiBaseUrl()
    expect(result).toBe('http://api:8000')
  })

  it('should fallback to NEXT_PUBLIC_API_BASE_URL in server context when API_INTERNAL_URL not set', () => {
    // Mock server environment
    delete (global as any).window
    
    process.env.NEXT_PUBLIC_API_BASE_URL = 'https://api.example.com'
    delete process.env.API_INTERNAL_URL

    // Import the function after setting up mocks
    const { getApiBaseUrl } = require('@/lib/api')
    
    const result = getApiBaseUrl()
    expect(result).toBe('https://api.example.com')
  })

  it('should use default localhost when no env vars set', () => {
    // Mock browser environment
    Object.defineProperty(window, 'window', {
      value: {},
      writable: true
    })
    
    delete process.env.NEXT_PUBLIC_API_BASE_URL
    delete process.env.API_INTERNAL_URL

    // Import the function after setting up mocks
    const { getApiBaseUrl } = require('@/lib/api')
    
    const result = getApiBaseUrl()
    expect(result).toBe('http://localhost:8000')
  })
})