<script lang="ts">
	import { createTaskFromTemplateRequest, createTaskRequest } from '$lib/api/task';
	import { getTaskTemplatesRequest } from '$lib/api/taskTemplates';
	import type { Task, TaskTemplate } from '$lib/api/model/task';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let parentTask: Task;

	let taskTemplates = getTaskTemplatesRequest();
	let selectedTemplate: TaskTemplate;
	let showModal = false;

	let taskName: string;

	let error: string = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		taskName = '';
	}

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

	<form slot="body" on:submit|preventDefault={createTask}>
		{#await taskTemplates}
			<Spinner />
		{:then taskTemplates}
			<div class="row g-3">
				<div class="col-12">
					<select id="templateSelect" class="form-select" bind:value={selectedTemplate}>
						<option value={null} disabled selected class="form-check-input"> -- Templates -- </option>
						{#each taskTemplates as template}
							<option value={template}>{template.name}</option>
						{/each}
					</select>
				</div>
				<div class="line-around">OR</div>
				<div class="col-12">
					<input placeholder="Task name" class="form-control" bind:value={taskName} />
				</div>
				<div class="col-12">
					<button type="submit" class="btn btn-primary">Create task</button>
				</div>
			</div>
			{#if error}
				<Error message={error} />
			{/if}
		{:catch error}
			<Error message={error.message} />
		{/await}
	</form>
</Modal>
