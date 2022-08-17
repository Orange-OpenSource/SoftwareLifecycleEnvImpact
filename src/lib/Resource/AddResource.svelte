<script lang="ts">
	import Modal from '$lib/Modal.svelte';
	import { getResourceTemplatesRequest } from '$lib/api/resourceTemplates';
	import type { Task, TaskTemplate } from 'src/model/task';
	import { addResourceRequest } from '$lib/api/resource';

	/*Bound var*/
	export let task: Task;

	let showModal = false;

	let resourceTemplates = getResourceTemplatesRequest();
	let selectedTemplate: TaskTemplate;

	async function handleSubmit() {
		if (selectedTemplate != null) {
			const res = await addResourceRequest(selectedTemplate.name, task.id, selectedTemplate.id);
			task.resources.push(res);
			/*Redondant assignment to force Svelte to update components*/
			task.resources = task.resources;
			showModal = false;
		}
	}
</script>

<input on:click={() => (showModal = true)} type="image" src="/add.svg" width="25" height="25" alt="Bin" loading="lazy" />

<Modal bind:showModal>
	<span slot="title">Create new resource :</span>
	<form slot="body" on:submit|preventDefault={handleSubmit}>
		{#await resourceTemplates}
			<div class="spinner-border" role="status" />
		{:then resourceTemplates}
			<select class="form-select" bind:value={selectedTemplate}>
				<option value={null} disabled selected class="form-check-input"> -- Templates -- </option>
				{#each resourceTemplates as template}
					<option value={template}>{template.name}</option>
				{/each}
			</select>
		{:catch error}
			<p style="color: red">{error.message}</p>
		{/await}

		<button type="submit" data-dismiss="modal" class="btn btn-primary">Create resource</button>
	</form>
</Modal>
