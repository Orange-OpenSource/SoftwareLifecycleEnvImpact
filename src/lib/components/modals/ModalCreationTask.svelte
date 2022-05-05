<script lang="ts">
	import Modal from './Modal.svelte';
	import { createTask } from '$lib/controllers/RequestController';
	import { createEventDispatcher } from 'svelte';

	export let task_id: any;
	export let model_id: any;
	const dispatch = createEventDispatcher();

	async function createNewTask(parentId: any) {
		// @ts-ignore
		let taskname = document.getElementById('createTaskInput' + parentId).value;

		await createTask(model_id, taskname, parentId, 0);

		dispatch('message', {
			text: 'updateTree'
		});
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateTask{task_id}" class="btn btn-primary">Add task</button>

<Modal details={'CreateTask' + task_id}>
	<span slot="title">Create new task :</span>
	<input slot="body" id="createTaskInput{task_id}" placeholder="Task name" required />
	<button on:click={() => createNewTask(task_id)} slot="btnsave" type="button" data-bs-dismiss="modal" class="btn btn-primary">Create task</button>
</Modal>
