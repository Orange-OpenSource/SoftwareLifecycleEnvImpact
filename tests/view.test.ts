import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	// Runs before each test and signs in each page.
	await page.goto('/');
	await page.fill('#email', 'test@test.fr');
	await page.fill('#password', 'test');
	await page.click('#login');
});

test('view/0 has expected 2 models', async ({ page }) => {
	await page.goto('/view/0');

	let listItems = page.locator('button.list-group-item > div');

	expect(await listItems.nth(0).textContent()).toBe(' Model 0 (default)  ');
	expect(await listItems.nth(1).textContent()).toBe(' Model 1   ');
});

test('view/0 has expected tasks', async ({ page }) => {
	await page.goto('/view/0');

	let listItems = page.locator('span.info-name');
	await listItems.nth(1).waitFor();

	expect(await listItems.nth(0).textContent()).toBe('Task 2');
	expect(await listItems.nth(1).textContent()).toBe('Task 3');
});
