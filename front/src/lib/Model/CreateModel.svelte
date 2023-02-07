<script lang="ts">
	import { createModelRequest } from '$lib/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model, Project } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';

	/* Bound vars */
	export let project: Project;
	export let selectedModel: Model;

	let showModal = false;

	let modelName: string;
	let error = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		modelName = '';
	}

	async function createModel() {
		if (modelName != undefined && modelName != '') {
			error = '';
			try {
				const res = await createModelRequest(modelName, project.id);
				modelName = '';
				project.models!.push(res);
				selectedModel = res;
				/*Redondant assignment to force Svelte to update components*/
				project.models = project.models;
				showModal = false;
			} catch (e: any) {
				error = e.message;
			}
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="btn btn-outline-primary">Add model</button>

<Modal bind:showModal>
	<span slot="title">Create new model</span>
	<form slot="body" on:submit|preventDefault={createModel}>
		<div class="row g-3">
			<div class="col-12">
				<input id="createModelInput" class="form-control" placeholder="Model name" required bind:value={modelName} />
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-primary">Create model</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
