<script lang="ts">
	import { duplicateModelRequest } from '$lib/model/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from '$lib/model/api/model/model';
	import Error from '$lib/Error.svelte';

	/*Bound var*/
	export let models: Model[];
	export let selectedModel: Model;

	export let model: Model;

	let showModal = false;
	let error = '';

	$: showModal, (error = ''); //Clean error message when closing modal

	async function duplicateModel() {
		error = '';
		try {
			const res = await duplicateModelRequest(model);
			models.push(res);
			selectedModel = res;
			/*Redundant assignement to force svelte to update components*/
			models = models;
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Duplicate</button>

<Modal bind:showModal>
	<span slot="title">Confirm duplicate</span>

	<span slot="body">Are you sure you want to duplicate <strong>{model.name}</strong> ?</span>

	{#if error}
		<Error message={error} slot="error" />
	{/if}

	<button on:click|stopPropagation={() => duplicateModel()} slot="btnsave" type="button" class="btn">Duplicate</button>
</Modal>
