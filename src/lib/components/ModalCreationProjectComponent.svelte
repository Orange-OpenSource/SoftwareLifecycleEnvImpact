<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/env';
	import { createProject } from '../controllers/RequestController';

	async function createNewProject() {
		// @ts-ignore
		let name = document.getElementById('createProjectInput').value;
		let newProjectId = await createProject(name);
		if (browser) {
			goto('/view/' + newProjectId);
		}
	}
</script>

<div
	class="modal fade"
	id="modalCreate"
	tabindex="-1"
	aria-labelledby="modalLabelCreate"
	aria-hidden="true"
>
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="modalLabelCreate">Create new project :</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>
			<div class="modal-body">
				<input id="createProjectInput" placeholder="Project name" required />
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
				<button
					on:click={createNewProject}
					type="button"
					data-bs-dismiss="modal"
					class="btn btn-primary">Create project</button
				>
			</div>
		</div>
	</div>
</div>
