<script lang="ts">
	import { createTaskRequest } from '$lib/api/task';
	import { getTaskTemplatesRequest } from '$lib/api/taskTemplates';
	import type { Model } from 'src/model/model';
	import type { Task, TaskTemplate } from 'src/model/task';
	import Modal from '../Modal.svelte';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';

	/* Bound var */
	export let parentTask: Task;

	export let selectedModel: Model;

	let taskTemplates = getTaskTemplatesRequest();
	let selectedTemplate: TaskTemplate;
	let showModal = false;

	let error = '';
	$: showModal, (error = ''); //Clean error message when closing modal

	async function handleSubmit() {
		error = '';
		try {
			if (selectedTemplate != null) {
				const res = await createTaskRequest(selectedModel.id, selectedTemplate.name, parentTask.id, selectedTemplate.id);
				parentTask.subtasks.push(res);
				/*Redondant assignment to force Svelte to update components*/
				parentTask.subtasks = parentTask.subtasks;
				showModal = false;
			}
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-primary">Add task</button>

{#await taskTemplates}
	<Spinner />
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
			{#if error}
				<Error message={error} slot="error"/>
			{/if}
			<button type="submit" class="btn btn-primary">Create task</button>
		</form>
	</Modal>
{:catch error}
	<Error message={error.message} />
{/await}
