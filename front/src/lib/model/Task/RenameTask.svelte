<script lang="ts">
	import type { Task } from '$lib/model/api/model/task';
	import Error from '$lib/Error.svelte';
	import { renameTaskRequest } from '$lib/model/api/task';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let task: Task;

	let showModal = false;
	let error = '';
	let newName = task.name;

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		newName = '';
	}

	async function renameTask() {
		error = '';
		try {
			const res = await renameTaskRequest(task, newName);
			task.name = res.name;
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<input on:click|stopPropagation={() => (showModal = true)} type="image" src="/pencil.svg" width="25" height="25" alt="Pencil" loading="lazy" />

<Modal bind:showModal>
	<span slot="title">Rename task</span>

	<form slot="body" on:submit|preventDefault={renameTask}>
		<div class="row g-3">
			<div class="col-12">
				<!-- TODO label ? -->
				<input class="form-control" placeholder="Task new name" required bind:value={newName} />
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-primary">Rename task</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
