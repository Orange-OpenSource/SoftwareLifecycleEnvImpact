<script>
	import { patch } from '$lib/api';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let model;

	let newName = model.name
	let showModal = false;
	let error = ''

	async function renameModel() {
		const res = await patch('models/' + model.id, [{
			op: 'replace',
			path: '/name',
			value: newName,
		}])
		switch (res.status) {
			case undefined:
				model.name = res.name
				showModal = false;
				break;
			case 403:
				error = 'Patch format is incorrect'
				break;
			case 404:
				error = 'No model found with this id' + model.id
				break;
			case 409:
				error = 'Model already exists'
				break;
			default:
				error = res.status + ' error'
				break;
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} type="button" class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename model :</span>
	<form slot="body" on:submit|preventDefault={renameModel}>
		<input id="renameModelInput{model.id}" placeholder="Model new name" bind:value={newName} required />

		{#if error != ''}
			<p style="color: red">{error}</p>
		{/if}

		<button type="submit" class="btn btn-primary">Rename model</button>
	</form>
	
</Modal>
