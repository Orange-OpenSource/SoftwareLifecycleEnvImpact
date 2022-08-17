<script lang="ts">
	import { createTaskRequest } from '$lib/api/task';
	import { getTaskTemplatesRequest } from '$lib/api/taskTemplates';
	import type { Model } from 'src/model/model';
	import type { Task, TaskTemplate } from 'src/model/task';
	import Modal from '../Modal.svelte';
	import Error from '$lib/Error.svelte'

	/* Bound var */
	export let parentTask: Task;

	export let selectedModel: Model;

	let taskTemplates = getTaskTemplatesRequest();
	let selectedTemplate: TaskTemplate;
	let showModal = false;

	let error = '';

	async function handleSubmit() {
		if (selectedTemplate != null) {
			const res = await createTaskRequest(selectedModel.id, selectedTemplate.name, parentTask.id, selectedTemplate.id);
			parentTask.subtasks.push(res)
			/*Redondant assignment to force Svelte to update components*/
			parentTask.subtasks = parentTask.subtasks
			showModal = false;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-primary">Add task</button>

{#await taskTemplates}
	<div class="spinner-border" role="status" />
{:then taskTemplates}
	<Modal bind:showModal>
		<span slot="title">Create new task :</span>
		<form slot="body" on:submit|preventDefault={handleSubmit}>
			<select id="templateSelect" class="form-select" bind:value={selectedTemplate}>
				<option value={null} disabled selected class="form-check-input"> -- Templates -- </option>
				{#each taskTemplates as template}
					<option value={template}>{template.name}</option>
				{/each}
			</select>
			{#if error != ''}
				<p style="color: red">{error}</p>
			{/if}
			<button type="submit" class="btn btn-primary">Create task</button>
		</form>
	</Modal>
{:catch error}
	<Error message={error.message}/>
{/await}
