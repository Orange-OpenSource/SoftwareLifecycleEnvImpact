<script>
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import { createProject } from '$lib/controllers/RequestController';
	import ModalComponent from '../Modal.svelte';

	let error = '';

	async function createNewProject() {
		let name = document.getElementById('createProjectInput').value;
		let newProject = await createProject(name);

		if (newProject.status === 409) {
			error = 'Project already exists';
		} else {
			document.querySelector('div.modal-backdrop.fade.show').remove();

			if (browser) goto('/view/' + newProject.id);
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreate" type="button" class="btn btn-light">New project</button>

<ModalComponent details={'Create'}>
	<span slot="title">Create new project</span>
	<div slot="body">
		<input id="createProjectInput" placeholder="Project name" required />
		{#if error}
			<div id="error_message" class="text-danger">
				<small>{error}</small>
			</div>
		{/if}
	</div>
	<button slot="btnsave" on:click={createNewProject} type="button" class="btn btn-primary">Create project</button>
</ModalComponent>
