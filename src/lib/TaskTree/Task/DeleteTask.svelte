<script>
    import { del } from '$lib/api';
	import ModalComponent from '$lib/Modal.svelte';

	/* Bound var */
	export let task;

	async function deleteTask() {
		const res = await del('tasks/'+task.id)

		if (res.status === 404) alert('No task with this id');
		else if (res.status === 403) alert('Cannot delete the root task of a model');
	}
</script>

<button on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalDeleteTask{task.id}" class="btn btn-light">Delete</button>

<ModalComponent details="DeleteTask{task.id}">
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{task.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteTask()} slot="btnsave" type="button" data-bs-dismiss="modal" class="btn btn-danger">Delete</button>
</ModalComponent>