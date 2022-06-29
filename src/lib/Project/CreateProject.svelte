<script>
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import Modal from '../Modal.svelte';
	import { post } from '$lib/api';

	let projectName;
	let showModal = false;

	async function createNewProject() {
		const res = await post('projects', {
			name: projectName
		})
		if (res.status === 409) {
			alert('Project exists already');
		} else {
			showModal = false
			if (browser) goto('/project/' + res.id); /*TODO useful ? */
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} type="button" class="btn btn-light">New project</button>

<Modal bind:showModal>
	<span slot="title">Create new project</span>
	<form slot="body" on:submit|preventDefault={createNewProject}>
		<input id="createProjectInput" placeholder="Project name" required bind:value={projectName}/>
		<button type="submit" class="btn btn-primary">Create project</button>
	</form>
</Modal>
