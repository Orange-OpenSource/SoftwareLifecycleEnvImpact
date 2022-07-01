<script>
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import Modal from '../Modal.svelte';
	import { post } from '$lib/api';

	let projectName;
	let showModal = false;
	let error = '';

	async function createNewProject() {
		const res = await post('projects', {
			name: projectName
		})
		switch (res.status) {
			case undefined:
				showModal = false
				if (browser) goto('/project/' + res.id); /*TODO useful ? */
				break;
			case 409:
				error = 'Project already exist'
				break;
			default:
				error = res.status + ' error'
				break;
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} type="button" class="btn btn-light">New project</button>

<Modal bind:showModal>
	<span slot="title">Create new project</span>
	<form slot="body" on:submit|preventDefault={createNewProject}>
		<input id="createProjectInput" placeholder="Project name" required bind:value={projectName}/>
        {#if error != ''}
            <p style="color: red">{error}</p>
        {/if}
		<button type="submit" class="btn btn-primary">Create project</button>
	</form>
</Modal>
