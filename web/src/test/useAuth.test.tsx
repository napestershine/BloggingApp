import { describe, it, expect, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useAuth } from '@/hooks/useAuth'
import { AuthProvider } from '@/components/AuthProvider'
import { ReactNode } from 'react'

// Mock the AuthProvider to avoid complex dependencies
vi.mock('@/components/AuthProvider', () => ({
  AuthProvider: ({ children }: { children: ReactNode }) => children,
  AuthContext: {
    Provider: ({ children, value }: { children: ReactNode; value: any }) => 
      <div data-testid="auth-context" data-value={JSON.stringify(value)}>{children}</div>
  }
}))

describe('useAuth', () => {
  it('throws error when used outside AuthProvider', () => {
    // Mock useContext to return undefined (outside provider)
    vi.doMock('react', async () => {
      const actual = await vi.importActual('react')
      return {
        ...actual,
        useContext: vi.fn(() => undefined)
      }
    })

    expect(() => {
      renderHook(() => useAuth())
    }).toThrow('useAuth must be used within an AuthProvider')
  })

  it('returns auth context when used within AuthProvider', () => {
    const mockAuthValue = {
      user: { id: 1, username: 'testuser', email: 'test@example.com' },
      isAuthenticated: true,
      login: vi.fn(),
      logout: vi.fn(),
      isLoading: false
    }

    // Mock useContext to return mock value
    vi.doMock('react', async () => {
      const actual = await vi.importActual('react')
      return {
        ...actual,
        useContext: vi.fn(() => mockAuthValue)
      }
    })

    const { result } = renderHook(() => useAuth())
    
    expect(result.current).toEqual(mockAuthValue)
  })
})