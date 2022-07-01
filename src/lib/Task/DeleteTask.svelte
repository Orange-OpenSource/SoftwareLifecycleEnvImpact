<script>
    import { del } from '$lib/api';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let parentTask

	export let task;
	let error = '';

	let showModal = false;

	async function deleteTask() {
		const res = await del('tasks/'+task.id)

		error = '' 
		switch (res.status) {
            case undefined:
				parentTask.subtasks = parentTask.subtasks.filter(s => s.id != task.id);
				/*Redondant assignment to force Svelte to update components*/
				parentTask.subtasks = parentTask.subtasks
				showModal = false;
				break;
			case 403:
				error = 'Cannot delete the root task of a model'
				break;
            case 404:
                error = 'No task with this id'
				break;
            default:
                error = res.status + ' error'
				break;
        }
	}
</script>

<button on:click|stopPropagation={() => showModal = true}  class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{task.name}</strong> ?</span>

	{#if error != ''}
		<p style="color: red">{error}</p>
	{/if}

	<button on:click|stopPropagation={() => deleteTask()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>