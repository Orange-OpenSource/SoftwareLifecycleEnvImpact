<script lang="ts">
	import { createTaskFromTemplateRequest, createTaskRequest } from '$lib/model/api/task';
	import { getTaskTemplatesRequest } from '$lib/model/api/taskTemplates';
	import type { Task, TaskTemplate } from '$lib/model/api/model/task';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import ResourceList from '$lib/model/Resource/ResourceList.svelte';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let parentTask: Task;

	let taskTemplates = getTaskTemplatesRequest();
	let selectedTemplate: TaskTemplate;
	let showModal = false;

	let taskName: string;

	let error: string = '';
	$: showModal,
		() => {
			error = '';
			taskName = '';
		}; //Clean error message when closing modal

	async function createTask() {
		error = '';
		try {
			let res;
			if (selectedTemplate != null) {
				res = await createTaskFromTemplateRequest(taskName != undefined && taskName != '' ? taskName : selectedTemplate.name, parentTask.id, selectedTemplate.id);
			} else if (taskName != undefined && taskName != '') {
				res = await createTaskRequest(taskName, parentTask.id);
			}

			if (res) {
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

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-primary">Add subtask</button>

<Modal bind:showModal>
	<span slot="title">Create new task :</span>
	<div slot="body">
		<form on:submit|preventDefault={createTask}>
			{#await taskTemplates}
				<Spinner />
			{:then taskTemplates}
				<select id="templateSelect" class="form-select" bind:value={selectedTemplate}>
					<option value={null} disabled selected class="form-check-input"> -- Templates -- </option>
					{#each taskTemplates as template}
						<option value={template}>{template.name}</option>
					{/each}
				</select>
				{#if error}
					<Error message={error} />
				{/if}
			{:catch error}
				<Error message={error.message} />
			{/await}

			<div class="line-around">OR</div>

			<input placeholder="Task name" bind:value={taskName} />

			<button type="submit" class="btn btn-primary">Create task</button>
		</form>
	</div>
</Modal>
