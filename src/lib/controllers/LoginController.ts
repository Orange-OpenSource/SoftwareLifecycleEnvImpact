import { user } from '../store';
import { browser } from '$app/env';
import { goto } from '$app/navigation';
import { onDestroy } from 'svelte';

/**
 * Check if the user is logged in.
 */
export async function checkIfLogged() {
	let user_value: any;
	user.subscribe((u) => (user_value = u));
	let unsubscribe = user.subscribe((u) => (user_value = u));

	if (!user_value) {
		if (browser) {
			goto('/login');
		}
	}

	onDestroy(unsubscribe);
}
