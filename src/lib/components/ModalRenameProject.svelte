<script lang="ts">
	import { getProjects, updateProject } from '$lib/controllers/RequestController';

	export let project_id: any;
	export let projects: any[] = [];

	async function renameProject() {
		// @ts-ignore
		let newName = document.getElementById('createProjectInput' + project_id).value;
		await updateProject(project_id, newName);
		projects = await getProjects();
	}
</script>

<div
	class="modal fade"
	id="modalRenameProject{project_id}"
	tabindex="-1"
	aria-labelledby="modalLabelRenameProject{project_id}"
	aria-hidden="true"
>
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="modalLabelRenameProject{project_id}">Rename project :</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>
			<div class="modal-body">
				<input id="createProjectInput{project_id}" placeholder="Project new name" required />
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
				<button
					on:click={renameProject}
					type="button"
					data-bs-dismiss="modal"
					class="btn btn-primary">Rename project</button
				>
			</div>
		</div>
	</div>
</div>
