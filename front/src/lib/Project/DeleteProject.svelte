<script lang="ts">
	import { deleteProjectRequest } from '$lib/api/project';
	import Modal from '$lib/Modal.svelte';
	import Error from '$lib/Error.svelte';
	import type { Project } from '$lib/api/dataModel';

	/* Bound var */
	export let projects: Project[];

	export let project: Project;

	let showModal = false;
	let error = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

	async function deleteProject() {
		error = '';
		try {
			await deleteProjectRequest(project);
			projects = projects.filter((p) => p.id != project.id);
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<form slot="body" on:submit|preventDefault={deleteProject}>
		<div class="row g-3">
			<div class="col-12">
				<p>Are you sure you want to delete project <strong>{project.name}</strong> ?</p>
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
