import { test, expect } from '@playwright/test'

test('user can navigate home page and view basic content', async ({ page }) => {
  // Navigate to home page
  await page.goto('/')

  // Check that the home page loads
  await expect(page).toHaveTitle(/Home/)
  
  // Verify hero section content exists
  await expect(page.getByRole('heading', { name: /Share Your Stories with the World/i })).toBeVisible()
  
  // Check navigation links exist
  await expect(page.getByText('Explore Posts')).toBeVisible()
  await expect(page.getByText('Start Writing')).toBeVisible()

  // Verify the page has some content structure
  await expect(page.locator('main')).toBeVisible()
})

test('page is responsive on mobile viewport', async ({ page }) => {
  // Set mobile viewport
  await page.setViewportSize({ width: 375, height: 667 })
  
  await page.goto('/')
  
  // Check that the page is responsive and content is still visible
  await expect(page.getByRole('heading', { name: /Share Your Stories with the World/i })).toBeVisible()
  
  // Verify mobile navigation works
  const exploreButton = page.getByText('Explore Posts')
  await expect(exploreButton).toBeVisible()
})