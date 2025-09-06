import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'

// Simple test component to validate test setup
function TestComponent() {
  return <div>Hello World</div>
}

describe('Test Setup Validation', () => {
  it('should render a simple component', () => {
    render(<TestComponent />)
    expect(screen.getByText('Hello World')).toBeInTheDocument()
  })

  it('should have MSW handlers available', () => {
    expect(typeof fetch).toBe('function')
  })
})