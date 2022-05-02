import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	// Runs before each test and signs in each page.
	await page.goto('/');
});

test('login page has expected error message when field are empty', async ({ page }) => {
	await page.click('#login');

	expect(await page.textContent('#error_message')).toBe('please enter your credentials');
});

test('login page has expected error message when field are false', async ({ page }) => {
	await page.fill('#email', 'baduser');
	await page.fill('#password', 'badpassword');
	await page.click('#login');

	expect(await page.textContent('#error_message')).toBe('Incorrect username and password');
});

test('login page show email when connected', async ({ page }) => {
	await page.fill('#email', 'test@test.fr');
	await page.fill('#password', 'test');
	await page.click('#login');

	await page.goto('/login');

	expect(await page.textContent('h2.title')).toBe('You are logged in as: test@test.fr');
});

test('login page has expected login form after logout', async ({ page }) => {
	await page.fill('#email', 'test@test.fr');
	await page.fill('#password', 'test');
	await page.click('#login');
	await page.goto('/login');
	await page.click('#logout');

	await expect(page.locator('input')).toHaveCount(2);
});
