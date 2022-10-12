<script lang="ts">
	import Modal from '$lib/Modal.svelte';
	import { getResourceTemplatesRequest } from '$lib/model/api/resourceTemplates';
	import type { Task, TaskTemplate } from '$lib/model/api/model/task';
	import { addResourceRequest } from '$lib/model/api/resource';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';

	/*Bound var*/
	export let task: Task;

	let showModal = false;

	let resourceTemplates = getResourceTemplatesRequest();
	let selectedTemplate: TaskTemplate;
	let name = '';

	let error = '';
	$: showModal,
		() => {
			error = '';
			name = '';
		}; //Clean error message when closing modal

	async function handleSubmit() {
		error = '';
		try {
			if (selectedTemplate != null) {
				const res = await addResourceRequest(name, task.id, selectedTemplate.id);
				task.resources.push(res);
				/*Redondant assignment to force Svelte to update components*/
				task.resources = task.resources;
				showModal = false;
			}
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-link">Add resource</button>

<Modal bind:showModal>
	<span slot="title">Add new resource :</span>
	<form slot="body" on:submit|preventDefault={handleSubmit}>
		{#await resourceTemplates}
			<Spinner />
		{:then resourceTemplates}
			<div class="row g-3">
				<div class="col-6">
					<input bind:value={name} type="text" class="form-control" placeholder="Name" required />
				</div>
				<div class="col-6">
					<select class="form-select" bind:value={selectedTemplate} required>
						<!-- <option value={null} disabled selected class="form-check-input"> -- Unit -- </option> -->
						{#each resourceTemplates as template}
							<option value={template} class="form-check-input">{template.name}</option>
						{/each}
					</select>
				</div>
				<div class="col-12">
					<button type="submit" data-dismiss="modal" class="btn btn-primary">Add resource</button>
				</div>
			</div>
		{:catch error}
			<Error message={error.message} />
		{/await}
	</form>
	{#if error}
		<Error message={error} />
	{/if}
</Modal>
