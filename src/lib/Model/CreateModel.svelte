<script lang="ts">
	import { createModelRequest } from '$lib/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from 'src/model/model';
	import type { Project } from 'src/model/project';
	import Error from '$lib/Error.svelte';

	/* Bound vars */
	export let project: Project;
	export let selectedModel: Model;

	let showModal = false;

	let modelName: string;
	let error = '';

	$: showModal, (error = ''); //Clean error message when closing modal

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

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="col-5 btn btn-light">Add model</button>

<Modal bind:showModal>
	<span slot="title">Create new model</span>
	<form slot="body" on:submit|preventDefault={createModel}>
		<input id="createModelInput" placeholder="Model name" required bind:value={modelName} />
		{#if error}
			<Error message={error} slot="error"/>
		{/if}
		<button type="submit" class="btn btn-primary">Create model</button>
	</form>
</Modal>
