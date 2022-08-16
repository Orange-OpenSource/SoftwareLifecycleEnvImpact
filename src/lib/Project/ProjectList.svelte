<script >
	import { getProjects } from '$lib/api/project';

	import CreateProject from '$lib/Project/CreateProject.svelte';
	import RenameProject from '$lib/Project/RenameProject.svelte';
	import { getLastUpdate } from '$lib/utils';
	import DeleteProject from './DeleteProject.svelte';

	let projects = getProjects();
</script>

<div>
	{#await projects}
		<div class="spinner-border" role="status" />
	{:then loadedProjects}
		{#each loadedProjects as project}
			<div class="list-group-item list-group-item-action">
				<div class="row">
					<div class="col">
						<a id="redirect{project.id}" sveltekit:prefetch href="/project/{project.id}">
							<h5 class="mb-1">
								{project.name}
							</h5>
							<small>{getLastUpdate(project)}</small>
						</a>
					</div>

					<div class="col">
						<RenameProject bind:project />
						<DeleteProject {project} />
					</div>
				</div>
			</div>
		{/each}
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}

	<CreateProject />
</div>
