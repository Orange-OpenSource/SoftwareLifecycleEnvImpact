import { writable } from 'svelte/store';
import { browser } from '$app/env';

const accepted_username = 'test@test.fr';
const accepted_password = 'test';

export const getUserDetails = async (user: string, pass: string) => {
	if (user === accepted_username && pass === accepted_password) return 1;
};

let persistedUser = browser && localStorage.getItem('user');
export let user = writable(persistedUser ? persistedUser : '');

if (browser) {
	user.subscribe((u) => (localStorage.user = u));
}
