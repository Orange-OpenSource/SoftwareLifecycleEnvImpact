<script lang="ts">
	import { deleteProjectRequest } from '$lib/api/project';
	import Modal from '$lib/Modal.svelte';
	import type { Project } from 'src/model/project';

	/* Bound var */
	export let projects: Project[];

	export let project: Project;

	let showModal = false;
	let error = '';

	async function deleteProject() {
		await deleteProjectRequest(project);
		projects = projects.filter((p) => p.id != project.id);
		showModal = false;
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{project.name}</strong> ?</span>

	{#if error != ''}
		<p style="color: red">{error}</p>
	{/if}

	<button on:click|stopPropagation={() => deleteProject()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
