<script lang="ts">
	import ModalComponent from './ModalComponent.svelte';
	import { createTask } from '$lib/controllers/RequestController';
	import { createEventDispatcher, onMount } from 'svelte';

	export let task_id: any;
	export let model_id: any;
	export let templates: any;

	const dispatch = createEventDispatcher();

	/**
	 * Create a new task with the given parent.
	 *
	 * @param parentId The parent id of the new task.
	 */
	async function createNewTask(parentId: any) {
		// @ts-ignore
		let taskname = document.getElementById('createTaskInput' + parentId).value;

		let newTask = await createTask(model_id, taskname, parentId);

		if (newTask.status === 409) alert('Task already exists on this level');
		else
			dispatch('message', {
				text: 'updateTree'
			});
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateTask{task_id}" class="btn btn-primary">Add task</button>

<ModalComponent details={'CreateTask' + task_id}>
	<span slot="title">Create new task :</span>
	<div slot="body">
		<select id="createTaskInput{task_id}" class="form-select">
			{#each templates as template}
				<option on:click={() => {}}>{template.name}</option>
			{/each}
		</select>
	</div>
	<button on:click={() => createNewTask(task_id)} data-bs-dismiss="modal" slot="btnsave" type="button" class="btn btn-primary">Create task</button>
</ModalComponent>
