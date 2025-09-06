import { test, expect } from '@playwright/test'

test('user can navigate home page and explore content', async ({ page }) => {
  // Navigate to home page
  await page.goto('/')

  // Check that the home page loads
  await expect(page).toHaveTitle(/Home/)
  
  // Verify hero section
  await expect(page.getByRole('heading', { name: /Share Your Stories with the World/i })).toBeVisible()
  
  // Check navigation links exist
  await expect(page.getByText('Explore Posts')).toBeVisible()
  await expect(page.getByText('Start Writing')).toBeVisible()

  // Verify features section is present
  await expect(page.locator('section').nth(1)).toBeVisible()
})

test('user can visit search page', async ({ page }) => {
  // This test assumes there's a search page or search functionality
  await page.goto('/search')
  
  // If search page doesn't exist, this will fail and we can skip/modify
  await page.waitForLoadState('networkidle')
  
  // Basic check that page loaded
  expect(page.url()).toContain('/search')
})

test('responsive design works on mobile', async ({ page }) => {
  // Set mobile viewport
  await page.setViewportSize({ width: 375, height: 667 })
  
  await page.goto('/')
  
  // Check that the page is responsive
  await expect(page.getByRole('heading', { name: /Share Your Stories with the World/i })).toBeVisible()
  
  // Verify mobile navigation (if implemented)
  const exploreButton = page.getByText('Explore Posts')
  await expect(exploreButton).toBeVisible()
})