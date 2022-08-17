<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import Modal from '../Modal.svelte';
	import { createProjectRequest } from '$lib/api/project';
	import Error from '$lib/Error.svelte';

	let projectName: string;
	let showModal = false;
	let error = '';

	$: showModal, error = '' //Clean error message when closing modal

	async function createNewProject() {
		error = ''
		try{
			const res = await createProjectRequest(projectName);
			showModal = false;
			if (browser) goto('/project/' + res.id);
		}catch(e: any){
			error = e.message
		} 
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="btn btn-light">New project</button>

<Modal bind:showModal>
	<span slot="title">Create new project</span>
	<form slot="body" on:submit|preventDefault={createNewProject}>
		<input id="createProjectInput" placeholder="Project name" required bind:value={projectName} />
		{#if error}
			<Error message={error} />
		{/if}
		<button type="submit" class="btn btn-primary">Create project</button>
	</form>
</Modal>
