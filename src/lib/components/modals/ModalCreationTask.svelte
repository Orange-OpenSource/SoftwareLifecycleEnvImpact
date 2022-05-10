<script lang="ts">
	import ModalComponent from './ModalComponent.svelte';
	import { createTask } from '$lib/controllers/RequestController';
	import { createEventDispatcher } from 'svelte';
	import { Modal } from 'bootstrap';

	export let task_id: any;
	export let model_id: any;
	const dispatch = createEventDispatcher();
	let error: string = '';

	async function createNewTask(parentId: any) {
		// @ts-ignore
		let taskname = document.getElementById('createTaskInput' + parentId).value;

		let newTask = await createTask(model_id, taskname, parentId, 0);

		if (newTask.status === 409) {
			error = 'Task already exists';
		} else {
			error = '';
			let myModal = document.getElementById('modalCreateTask' + task_id)!;
			let modal = Modal.getInstance(myModal);
			modal!.hide();
			document.querySelector('div.modal-backdrop.fade.show')!.remove();

			dispatch('message', {
				text: 'updateTree'
			});
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateTask{task_id}" class="btn btn-primary">Add task</button>

<ModalComponent details={'CreateTask' + task_id}>
	<span slot="title">Create new task :</span>
	<div slot="body">
		<input id="createTaskInput{task_id}" placeholder="Task name" required />
		{#if error}
			<div id="error_message" class="text-danger">
				<small>{error}</small>
			</div>
		{/if}
	</div>
	<button on:click={() => createNewTask(task_id)} slot="btnsave" type="button" class="btn btn-primary">Create task</button>
</ModalComponent>
