<script lang="ts">
	import { getProjects, updateProject } from '$lib/controllers/RequestController';
	import Modal from './Modal.svelte';

	export let project_id: any;
	export let projects: any[] = [];

	async function renameProject() {
		// @ts-ignore
		let newName = document.getElementById('createProjectInput' + project_id).value;
		await updateProject(project_id, newName);
		projects = await getProjects();
	}
</script>

<button
	data-bs-toggle="modal"
	data-bs-target="#modalRenameProject{project_id}"
	type="button"
	class="btn btn-outline-secondary btn-sm">Rename</button
>

<Modal details={'RenameProject' + project_id}>
	<span slot="title">Rename project :</span>
	<input slot="body" id="createProjectInput{project_id}" placeholder="Project new name" required />
	<button
		slot="btnsave"
		on:click={renameProject}
		type="button"
		data-bs-dismiss="modal"
		class="btn btn-primary">Rename project</button
	>
</Modal>
