<script lang="ts">
	import { renameProjectRequest } from '$lib/api/project';
	import type { Project } from 'src/model/models';
	import Modal from '../Modal.svelte';

	/* Bound var */
	export let project: Project;

	let newName = project.name;
	let showModal = false;

	let error = '';

	async function renameProject() {
		const res = await renameProjectRequest(project, newName);

		project.name = res.name;
		showModal = false;
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename project :</span>
	<form slot="body" on:submit|preventDefault={renameProject}>
		<input id="renameProjectInput{project.id}" placeholder="Project new name" bind:value={newName} required />

		{#if error != ''}
			<p style="color: red">{error}</p>
		{/if}
		<button type="submit" class="btn btn-primary">Rename project</button>
	</form>
</Modal>
