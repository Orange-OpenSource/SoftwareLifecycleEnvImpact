<script lang="ts">
	import type { Project } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';
	import { renameProjectRequest } from '$lib/api/project';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let project: Project;

	let newName = project.name;
	let showModal = false;

	let error = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		newName = project.name;
	}

	async function renameProject() {
		error = '';
		try {
			const res = await renameProjectRequest(project, newName);
			project.name = res.name;
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename project :</span>

	<form slot="body" on:submit|preventDefault={renameProject}>
		<div class="row g-3">
			<div class="col-12">
				<input class="form-control" placeholder="Project new name" required bind:value={newName} />
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-primary">Rename project</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
