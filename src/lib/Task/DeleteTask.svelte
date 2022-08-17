<script lang="ts">
	import { deleteTaskRequest } from '$lib/api/task';
	import Modal from '$lib/Modal.svelte';
	import type { Task } from 'src/model/task';

	/* Bound var */
	export let parentTask: Task;

	export let task: Task;

	let error = '';

	let showModal = false;

	async function deleteTask() {
		await deleteTaskRequest(task);
		parentTask.subtasks = parentTask.subtasks.filter(s => s.id != task.id);
		/*Redondant assignment to force Svelte to update components*/
		parentTask.subtasks = parentTask.subtasks;
		showModal = false;
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{task.name}</strong> ?</span>

	{#if error != ''}
		<p style="color: red">{error}</p>
	{/if}

	<button on:click|stopPropagation={() => deleteTask()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
