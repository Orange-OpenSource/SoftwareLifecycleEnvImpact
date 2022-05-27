<script>
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import ModalComponent from '../Modal.svelte';
	import { post } from '$lib/api';

	let error = '';

	async function createNewProject() {
		let nameProject = document.getElementById('createProjectInput').value;

		const res = await post('projects', {
			name: nameProject
		})
		if (res.status === '409') {
			alert('Project exists already');
		} else {
			document.querySelector('div.modal-backdrop.fade.show').remove();

			if (browser) goto('/project/' + res.id); /*TODO useful ? */
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
