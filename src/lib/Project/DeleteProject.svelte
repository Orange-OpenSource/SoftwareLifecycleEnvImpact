<script lang="ts">
	import { del } from '$lib/api/api';
	import Modal from '$lib/Modal.svelte';
	import type { Project } from 'src/model/models';

	/* Bound var */
	/*TODO delete from projects list*/
	//export let projects: Promise<Project[]>;

	export let project: Project;

	let showModal = false;
	let error = '';

	async function deleteProject(projectToDelete: Project) {
		const res = await del('projects/' + projectToDelete.id);

		switch (res.status) {
			case undefined:
				/*TODO delete project from list*/
				//projects = projects.filter(p => p.id != projectToDelete.id);
				showModal = false;
				break;
			case 404:
				error = 'No project found with this id ' + project.id;
				break;
			default:
				error = res.status + ' error';
				break;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{project.name}</strong> ?</span>

	{#if error != ''}
		<p style="color: red">{error}</p>
	{/if}

	<button on:click|stopPropagation={() => deleteProject(project)} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
