<script>
	import { onMount } from 'svelte';
	import { deleteProject } from '$lib/controllers/RequestController';
	import CreateProject from '$lib/Project/CreateProject.svelte';
	import RenameProject from '$lib/Project/RenameProject.svelte';
	import { getCreationDate } from '$lib/utils';
	import { get } from '$lib/api';

	let projects = [];

	/**
	 * Delete the project in API and update page without it.
	 *
	 * @param project_id
	 */
	async function deleteProjectInAPI(project) {
		await deleteProject(project);
	}

	onMount(async function () {
		projects = await get('projects')
	});
</script>

<div>
	<ul class="list-group list-group-flush" style="margin-bottom : 5px;">
		{#each projects as project}
			<li class="list-group-item">
				<div class="card-body d-flex justify-content-center">
					<div class="d-flex justify-content-between" style="width: 40%;">
						<a id="redirect{project.id}" sveltekit:prefetch href="/project/{project.id}">{project.name}</a>
						<div>
							<RenameProject {project} />
							<button on:click={() => deleteProjectInAPI(project)} type="button" class="btn btn-outline-danger btn-sm">Delete</button>
						</div>
					</div>
				</div>
				<span class="d-flex justify-content-center" style="color:grey; font-size : 12px">Created at : {getCreationDate(project.created_at)}</span>
			</li>
		{/each}
	</ul>

	<CreateProject />
</div>
