<script lang="ts">
	import type { Project } from '$lib/model/api/model/project';
	import Error from '$lib/Error.svelte';
	import { renameProjectRequest } from '$lib/model/api/project';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let project: Project;

	let newName = project.name;
	let showModal = false;

	let error = '';

	$: showModal, (error = ''); //Clean error message when closing modal

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
		<input id="renameProjectInput{project.id}" placeholder="Project new name" bind:value={newName} required />

		{#if error}
			<Error message={error} slot="error" />
		{/if}
		<button type="submit" class="btn btn-primary">Rename project</button>
	</form>
</Modal>
