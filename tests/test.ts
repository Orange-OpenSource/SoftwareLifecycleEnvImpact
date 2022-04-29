import { expect, test } from '@playwright/test';

test('index page has expected div header', async ({ page }) => {
	await page.goto('/');
	expect(await page.textContent('div#header')).toBe(
		'Software Lifecycle Environmental Impact Profile Home'
	);
});
