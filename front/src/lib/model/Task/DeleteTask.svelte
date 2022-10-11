<script lang="ts">
	import { deleteTaskRequest } from '$lib/model/api/task';
	import Modal from '$lib/Modal.svelte';
	import type { Task } from '$lib/model/api/model/task';
	import Error from '$lib/Error.svelte';

	/* Bound var */
	export let parentTask: Task;

	export let task: Task;

	let showModal = false;

	let error = '';
	$: showModal, (error = ''); //Clean error message when closing modal

	async function deleteTask() {
		error = '';
		try {
			await deleteTaskRequest(task);
			parentTask.subtasks = parentTask.subtasks.filter((s) => s.id != task.id);
			/*Redondant assignment to force Svelte to update components*/
			parentTask.subtasks = parentTask.subtasks;
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<input on:click|stopPropagation={() => (showModal = true)} type="image" src="/trash.svg" width="25" height="25" alt="Bin" loading="lazy" />

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{task.name}</strong> ?</span>

	{#if error}
		<Error message={error} slot="error" />
	{/if}

	<button on:click|stopPropagation={() => deleteTask()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
