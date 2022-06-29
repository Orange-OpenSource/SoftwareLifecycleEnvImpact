<script>
    import { del } from '$lib/api';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let parentTask

	export let task;

	let showModal = false;

	async function deleteTask() {
		const res = await del('tasks/'+task.id)

		if (res.status === 404) alert('No task with this id');
		else if (res.status === 403) alert('Cannot delete the root task of a model');
		else{
			parentTask.subtasks = parentTask.subtasks.filter(s => s.id != task.id);
			/*Redondant assignment to force Svelte to update components*/
			parentTask.subtasks = parentTask.subtasks
			showModal = false;
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true}  class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{task.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteTask()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>