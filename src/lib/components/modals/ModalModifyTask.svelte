<script lang="ts">
	import { deleteTask, getTemplates, updateTask } from '$lib/controllers/RequestController';
	import { createEventDispatcher, onMount } from 'svelte';
	import ModalComponent from './ModalComponent.svelte';

	export let task: any;
	export let tasks: any[];
	export let classAttribute: string;
	export let templates: any;

	const dispatch = createEventDispatcher();

	/**
	 * Delete task within the id "task.id".
	 */
	async function deleteTaskInAPI() {
		await deleteTask(task.id);

		dispatch('message', {
			text: 'updateTree'
		});
	}

	/**
	 * Update the parent of task.id to idParent.
	 */
	async function updateParent(idParent: any) {
		console.log(idParent);
	}

	async function updateTaskInAPI(template: string) {
		await updateTask(task.id, template);

		dispatch('message', {
			text: 'updateTree'
		});
	}

	/**
	 * Set the "<select>" tag on the current parent by default.
	 *
	 * @param parentTask
	 */
	function isParent(parentTask: { id: any }) {
		return task.parent_task_id === parentTask.id;
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalModifyTask{task.id}" type="button" class="btn btn-outline-primary btn-sm {classAttribute}">Modify</button>

<ModalComponent details={'ModifyTask' + task.id}>
	<select slot="title" class="form-select">
		{#each templates as template}
			<option
				on:click={() => {
					updateTaskInAPI(template);
				}}
				value={template}>{template}</option
			>
		{/each}
	</select>
	<button slot="btndelete" on:click={deleteTaskInAPI} type="button" class="btn btn-danger btn-sm" data-bs-dismiss="modal">Delete</button>
	<div slot="body">
		Parent :
		<select class="form-select" aria-label="Default select example">
			{#each tasks as currentTask}
				{#if currentTask.id !== task.id}
					<option on:click={() => updateParent(currentTask.id)} selected={isParent(currentTask)}>{currentTask.name}</option>
				{/if}
			{/each}
		</select>

		<span id="task_id{task.id}">
			{#each task.inputs as input}
				<label for="taskinput">{input.name}</label>
				{#if input.kind == 'string'}
					<input class="input-group" type="text" id="taskinput" name="taskinput{input.id}" required />
				{:else if input.kind == 'float'}
					<input class="input-group" type="number" id="taskinput" name="taskinput{input.id}" required />
				{:else}
					Not implemented
				{/if}
			{/each}
		</span>
	</div>
</ModalComponent>
