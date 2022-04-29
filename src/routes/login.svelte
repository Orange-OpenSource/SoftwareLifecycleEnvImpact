<script lang="ts">
	import { user, getUserDetails } from '../store';
	import { onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	let user_value: any;
	user.subscribe((u) => (user_value = u));
	let unsubscribe = user.subscribe((u) => (user_value = u));
	let email: any;
	let password: any;
	let error: string;
	async function handleLogin() {
		if (!email || !password) {
			error = 'please enter your credentials';
			return;
		}

		if (await getUserDetails(email, password)) {
			user.update((u) => (u = JSON.stringify({ email: email, password: password })));

			if (browser) {
				goto('/');
			}
		} else {
			error = 'Incorrect username and password';
			return;
		}
	}
	function handleLogout() {
		user.update((u) => (u = ''));
	}
	//$: console.log(user_value)
	onDestroy(unsubscribe);
</script>

<svelte:head>
	<title>Local Storage Stores Login</title>
</svelte:head>

{#if !user_value}
	<div class="mb-3">
		<label for="username" class="form-label">Username</label>
		<input type="email" bind:value={email} placeholder="enter email" />
	</div>
	<div class="mb-3">
		<label for="password" class="form-label">Password</label>
		<input type="password" bind:value={password} placeholder="enter password" />
	</div>

	<button type="submit" class="btn btn-primary" on:click={handleLogin}>Login</button>

	{#if error}
		<div id="error_message" class="text-danger">
			<small>{error}</small>
		</div>
	{/if}
{:else if user_value}
	<h2 class="title">You are logged in as: {JSON.parse(user_value).email}</h2>
	<button type="submit" class="btn btn-primary" on:click={handleLogout}>Logout</button>
{/if}
