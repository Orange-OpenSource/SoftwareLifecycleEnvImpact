<script lang="ts">
	import { getProjects, updateProject } from '$lib/controllers/RequestController';
	import ModalComponent from './ModalComponent.svelte';

	/* Bound var */
	export let project: any;
	export let projects: any[] = [];

	/**
	 * Rename project within the id "project.id".
	 */
	async function renameProject() {
		// @ts-ignore
		let newName = document.getElementById('createProjectInput' + project.id).value;
		await updateProject(project.id, newName);
		projects = await getProjects();
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalRenameProject{project.id}" type="button" class="btn btn-outline-secondary btn-sm">Rename</button>

<ModalComponent details={'RenameProject' + project.id}>
	<span slot="title">Rename project :</span>
	<input slot="body" id="createProjectInput{project.id}" placeholder="Project new name" value={project.name} required />
	<button slot="btnsave" on:click={renameProject} type="button" data-bs-dismiss="modal" class="btn btn-primary">Rename project</button>
</ModalComponent>
