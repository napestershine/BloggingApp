import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { getApiBaseUrl } from '@/lib/api'

describe('API Base URL Resolution', () => {
  // Store original process.env values
  let originalEnv: typeof process.env
  const originalWindow = globalThis.window

  beforeEach(() => {
    originalEnv = { ...process.env }
  })

  afterEach(() => {
    process.env = originalEnv
    Object.defineProperty(globalThis, 'window', {
      value: originalWindow,
      configurable: true,
      writable: true,
    })
  })

  it('should use NEXT_PUBLIC_API_BASE_URL in browser context', () => {
    Object.defineProperty(globalThis, 'window', {
      value: originalWindow ?? {},
      configurable: true,
      writable: true,
    })
    process.env.NEXT_PUBLIC_API_BASE_URL = 'https://api.example.com'
    process.env.API_INTERNAL_URL = 'http://api:8000'
    
    const result = getApiBaseUrl()
    expect(result).toBe('https://api.example.com')
  })

  it('should use API_INTERNAL_URL in server context', () => {
    Object.defineProperty(globalThis, 'window', {
      value: undefined,
      configurable: true,
      writable: true,
    })
    process.env.NEXT_PUBLIC_API_BASE_URL = 'https://api.example.com'
    process.env.API_INTERNAL_URL = 'http://api:8000'
    
    const result = getApiBaseUrl()
    expect(result).toBe('http://api:8000')
  })

  it('should fallback to NEXT_PUBLIC_API_BASE_URL in server context when API_INTERNAL_URL not set', () => {
    Object.defineProperty(globalThis, 'window', {
      value: undefined,
      configurable: true,
      writable: true,
    })
    process.env.NEXT_PUBLIC_API_BASE_URL = 'https://api.example.com'
    delete process.env.API_INTERNAL_URL
    
    const result = getApiBaseUrl()
    expect(result).toBe('https://api.example.com')
  })

  it('should use default localhost when no env vars set', () => {
    Object.defineProperty(globalThis, 'window', {
      value: originalWindow ?? {},
      configurable: true,
      writable: true,
    })
    delete process.env.NEXT_PUBLIC_API_BASE_URL
    delete process.env.API_INTERNAL_URL
    
    const result = getApiBaseUrl()
    expect(result).toBe('http://localhost:8000')
  })
})
