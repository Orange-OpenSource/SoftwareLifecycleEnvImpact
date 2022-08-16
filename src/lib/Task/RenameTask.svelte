<script lang="ts">
	import { renameTaskRequest } from '$lib/api/task';
	import type { Task } from 'src/model/task';
	import Modal from '../Modal.svelte';

	/* Bound var */
	export let task: Task;

	let showModal = false;

	let newName = task.name

	async function renameTask() {
		await renameTaskRequest(task, newName);
		/*TODO update task name*/
		showModal = false;
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename task</span>
	<form slot="body" on:submit|preventDefault={renameTask}>
		<input id="renameTask" placeholder="Task name" required bind:value={newName} />
		<button type="submit" class="btn btn-primary">Rename task</button>
	</form>
</Modal>
