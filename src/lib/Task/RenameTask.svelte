<script lang="ts">
	import { renameTaskRequest } from '$lib/api/task';
	import type { Task } from 'src/model/task';
	import Modal from '../Modal.svelte';
	import Error from '$lib/Error.svelte';

	/* Bound var */
	export let task: Task;

	let showModal = false;
	let error = '';
	let newName = task.name;

	$: showModal, error = '' //Clean error message when closing modal

	async function renameTask() {
		error = ''
		try{
			const res = await renameTaskRequest(task, newName);
			task.name = res.name;
			showModal = false;
		}catch(e: any){
			error = e.message
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename task</span>
	<form slot="body" on:submit|preventDefault={renameTask}>
		<input id="renameTask" placeholder="Task name" required bind:value={newName} />
		{#if error}
			<Error message={error} />
		{/if}
		<button type="submit" class="btn btn-primary">Rename task</button>
	</form>
</Modal>
