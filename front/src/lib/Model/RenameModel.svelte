<script lang="ts">
	import { renameModelRequest } from '$lib/api/model';
	import Modal from '$lib/Modal.svelte';
	import Error from '$lib/Error.svelte';
	import Icon from '@iconify/svelte';
	import type { Model } from '$lib/api/dataModel';

	/* Bound var */
	export let model: Model;

	let newName = model.name;
	let showModal = false;
	let error = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		newName = model.name;
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

<button class="btn btn-sm" on:click|stopPropagation={() => (showModal = true)}>
	<Icon icon="material-symbols:edit-outline" width="25" height="25" alt="Edit" loading="lazy" />
</button>

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
