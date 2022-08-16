<script lang="ts">
	import { createTask } from '$lib/api/task';
import { getTaskTemplates } from '$lib/api/task_templates';
	import type { Model } from 'src/model/model';
	import type { Task } from 'src/model/task';
	import type { TaskTemplate } from 'src/model/taskTemplate';
	import Modal from '../Modal.svelte';

	/* Bound var */
	export let parentTask: Task;

	export let selectedModel: Model;

	let taskTemplates = getTaskTemplates();
	let selectedTemplate: TaskTemplate;
	let showModal = false;

	let error = '';

	async function handleSubmit() {
		if (selectedTemplate != null) {
			await createTask(selectedModel.id, selectedTemplate.name, parentTask.id, selectedTemplate.id);

			/*TODO delete from parent task subtasks*/
			//parentTask.subtasks.push(res)
			/*Redondant assignment to force Svelte to update components*/
			//parentTask.subtasks = parentTask.subtasks
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
	<p style="color: red">{error.message}</p>
{/await}
