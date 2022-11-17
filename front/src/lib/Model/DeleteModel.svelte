<script lang="ts">
	import { deleteModelRequest } from '$lib/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';

	/*Bound var*/
	export let models: Model[];

	export let model: Model;

	let showModal = false;
	let error = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

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

	<form slot="body" on:submit|preventDefault={deleteModel}>
		<div class="row g-3">
			<div class="col-12">
				<p>Are you sure you want to delete <strong>{model.name}</strong> ?</p>
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-danger">Delete</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
