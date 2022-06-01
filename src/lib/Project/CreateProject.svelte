<script>
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import ModalComponent from '../Modal.svelte';
	import { post } from '$lib/api';

	let projectName;

	async function createNewProject() {
		const res = await post('projects', {
			name: projectName
		})
		if (res.status === 409) {
			alert('Project exists already');
		} else {
			if (browser) goto('/project/' + res.id); /*TODO useful ? */
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreate" type="button" class="btn btn-light">New project</button>

<ModalComponent details={'Create'}>
	<span slot="title">Create new project</span>
	<form slot="body" on:submit|preventDefault={createNewProject}>
		<input id="createProjectInput" placeholder="Project name" required bind:value={projectName}/>
		<button data-bs-dismiss="modal" type="submit" class="btn btn-primary">Create project</button>
	</form>
	
</ModalComponent>
