import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	// Runs before each test and signs in each page.
	await page.goto('/');
	await page.fill('#email', 'test@test.fr');
	await page.fill('#password', 'test');
	await page.click('#login');
});

test('index page has expected header', async ({ page }) => {
	expect(await page.textContent('div#header')).toBe(
		'Software Lifecycle Environmental Impact Profile Home'
	);
});

test('index page has expected projects', async ({ page }) => {
	expect(await page.textContent('h2')).toBe('My projects');

	let listItems = page.locator('ul > li');
	await listItems.nth(2).waitFor();

	for (let i = 0; i < 2; i++)
		expect(await listItems.nth(i).textContent()).toBe('Project ' + i + ' ');
});

test('index page has expected "New project" button', async ({ page }) => {
	expect(await page.textContent('button')).toBe('New project');
});
