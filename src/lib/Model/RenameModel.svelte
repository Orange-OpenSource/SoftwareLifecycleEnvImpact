<script lang="ts">
	import { renameModelRequest } from '$lib/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from 'src/model/model';
	import Error from '$lib/Error.svelte';

	/* Bound var */
	export let model: Model;

	let newName = model.name;
	let showModal = false;
	let error = '';

	$: showModal, (error = ''); //Clean error message when closing modal

	async function renameModel() {
		error = '';
		try {
			const res = await renameModelRequest(model, newName);
			model.name = res.name;
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename model :</span>
	<form slot="body" on:submit|preventDefault={renameModel}>
		<input id="renameModelInput{model.id}" placeholder="Model new name" bind:value={newName} required />

		{#if error}
			<Error message={error} slot="error" />
		{/if}

		<button type="submit" class="btn btn-primary">Rename model</button>
	</form>
</Modal>
