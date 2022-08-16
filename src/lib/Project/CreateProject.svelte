<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import Modal from '../Modal.svelte';
	import { createProject } from '$lib/api/project';

	let projectName: string;
	let showModal = false;
	let error = '';

	async function createNewProject() {
		const res = await createProject(projectName);
		showModal = false;
		if (browser) goto('/project/' + res.id);
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="btn btn-light">New project</button>

<Modal bind:showModal>
	<span slot="title">Create new project</span>
	<form slot="body" on:submit|preventDefault={createNewProject}>
		<input id="createProjectInput" placeholder="Project name" required bind:value={projectName} />
		{#if error != ''}
			<p style="color: red">{error}</p>
		{/if}
		<button type="submit" class="btn btn-primary">Create project</button>
	</form>
</Modal>
