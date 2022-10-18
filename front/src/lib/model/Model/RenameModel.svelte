<script lang="ts">
	import { renameModelRequest } from '$lib/model/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from '$lib/model/api/model/model';
	import Error from '$lib/Error.svelte';

	/* Bound var */
	export let model: Model;

	let newName = model.name;
	let showModal = false;
	let error = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

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

<input on:click|stopPropagation={() => (showModal = true)} type="image" src="/pencil.svg" width="25" height="25" alt="Pencil" loading="lazy" />

<Modal bind:showModal>
	<span slot="title">Rename model</span>

	<form slot="body" on:submit|preventDefault={renameModel}>
		<div class="row g-3">
			<div class="col-12">
				<!-- TODO label ? -->
				<input class="form-control" placeholder="Model new name" required bind:value={newName} />
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-primary">Rename model</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
