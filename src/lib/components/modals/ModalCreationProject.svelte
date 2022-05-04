<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import { createProject } from '$lib/controllers/RequestController';
	import Modal from './Modal.svelte';

	async function createNewProject() {
		// @ts-ignore
		let name = document.getElementById('createProjectInput').value;
		let newProjectId = await createProject(name);
		if (browser) {
			goto('/view/' + newProjectId);
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreate" type="button" class="btn btn-light"
	>New project</button
>

<Modal details={'Create'}>
	<span slot="title">Create new project</span>
	<input slot="body" id="createProjectInput" placeholder="Project name" required />
	<button
		slot="btnsave"
		on:click={createNewProject}
		type="button"
		data-bs-dismiss="modal"
		class="btn btn-primary">Create project</button
	>
</Modal>
