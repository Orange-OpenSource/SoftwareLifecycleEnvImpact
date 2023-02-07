<script lang="ts">
	import { deleteTaskRequest } from '$lib/api/task';
	import Modal from '$lib/Modal.svelte';
	import Error from '$lib/Error.svelte';
	import type { Task } from '$lib/api/dataModel';
	import Icon from '@iconify/svelte';

	/* Bound var */
	export let parentTask: Task;
	export let selectedTask: Task;

	export let task: Task;

	let showModal = false;

	let error = '';
	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

	async function deleteTask() {
		error = '';
		try {
			await deleteTaskRequest(task);
			parentTask.subtasks = parentTask.subtasks.filter((s) => s.id != task.id);
			/*Redondant assignment to force Svelte to update components*/
			parentTask.subtasks = parentTask.subtasks;
			if (task.id == selectedTask.id) {
				selectedTask = parentTask;
			}
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button class="btn" on:click|stopPropagation={() => (showModal = true)}>
	<Icon icon="ion:trash-outline" width="25" height="25" alt="Delete" loading="lazy" />
</button>
<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<form slot="body" on:submit|preventDefault={deleteTask}>
		<div class="row g-3">
			<div class="col-12">
				<p>Are you sure you want to delete task <strong>{task.name}</strong> ?</p>
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-danger">Delete</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
