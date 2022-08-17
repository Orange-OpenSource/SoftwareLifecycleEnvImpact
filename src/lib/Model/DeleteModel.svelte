<script lang="ts">
	import { deleteModelRequest } from '$lib/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from 'src/model/model';

	/*Bound var*/
	export let models: Model[];

	export let model: Model;

	let showModal: boolean;
	let error = '';

	async function deleteModel() {
		const res = await deleteModelRequest(model);
		models = models.filter(m => m.id != model.id);
		showModal = false;
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>

	{#if error != ''}
		<p style="color: red">{error}</p>
	{/if}

	<button on:click|stopPropagation={() => deleteModel()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
