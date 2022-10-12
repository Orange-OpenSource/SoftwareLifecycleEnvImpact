<script lang="ts">
	import { deleteModelRequest } from '$lib/model/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from '$lib/model/api/model/model';
	import Error from '$lib/Error.svelte';

	/*Bound var*/
	export let models: Model[];

	export let model: Model;

	let showModal = false;
	let error = '';

	$: showModal, (error = ''); //Clean error message when closing modal

	async function deleteModel() {
		error = '';
		try {
			await deleteModelRequest(model);
			models = models.filter((m) => m.id != model.id);
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<input on:click|stopPropagation={() => (showModal = true)} type="image" src="/trash.svg" width="25" height="25" alt="Trash" loading="lazy" />

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>

	{#if error}
		<Error message={error} slot="error" />
	{/if}

	<button on:click|stopPropagation={() => deleteModel()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
