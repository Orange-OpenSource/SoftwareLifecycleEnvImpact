<script lang="ts">
	import { deleteProjectRequest } from '$lib/model/api/project';
	import Modal from '$lib/Modal.svelte';
	import type { Project } from '$lib/model/api/model/project';
	import Error from '$lib/Error.svelte';

	/* Bound var */
	export let projects: Project[];

	export let project: Project;

	let showModal = false;
	let error = '';

	$: showModal, (error = ''); //Clean error message when closing modal

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

	<span slot="body">Are you sure you want to delete <strong>{project.name}</strong> ?</span>

	{#if error}
		<Error message={error} slot="error" />
	{/if}

	<button on:click|stopPropagation={() => deleteProject()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
