<script>
	import { getUserDetails } from '../stores';
	import { store } from '../stores';

	let username = '';
	let password = '';
	let error = ''

	async function login() {
		const user = await getUserDetails( username, password )

		if ( user ) {
			console.log(user)
			$store = user
			if ( error ) error = ''
		}
		else {
			error = 'Incorrect username and password.'
			console.log("Incorrect username and password.")
		}

	}

</script>

<form on:submit|preventDefault={login} class="flex mx-auto col-6">

	<div class="mb-3">
		<label for="username" class="form-label">Username</label>
		<input type="email" class="form-control" id="username" bind:value={username} />
	</div>

	<div class="mb-3">
		<label for="password" class="form-label">Password</label>
		<input type="password" class="form-control" id="password" bind:value={password} />
	</div>

	<button type="submit" class="btn btn-primary">Submit</button>
	<div id="error_message" class="text-danger">
		<small>{error}</small>
	</div>

</form>
