import { describe, it, expect, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useAuth } from '@/hooks/useAuth'
import { ReactNode } from 'react'
import { AuthContext } from '@/components/AuthProvider'

describe('useAuth', () => {
  it('throws error when used outside AuthProvider', () => {
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

    const wrapper = ({ children }: { children: ReactNode }) => (
      <AuthContext.Provider value={mockAuthValue as any}>
        {children}
      </AuthContext.Provider>
    )

    const { result } = renderHook(() => useAuth(), { wrapper })
    
    expect(result.current).toEqual(mockAuthValue)
  })
})
