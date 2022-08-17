<script lang="ts">
	import { onMount } from 'svelte';
	import { getProjectsRequest } from '$lib/api/project';
	import CreateProject from '$lib/Project/CreateProject.svelte';
	import RenameProject from '$lib/Project/RenameProject.svelte';
	import { getLastUpdate } from '$lib/utils';
	import DeleteProject from './DeleteProject.svelte';
	import type { Project } from 'src/model/project';

	let projects: Project[];
	let error: Error;

	onMount(async () => {
		/**
		 * Cannot use svelte promise logic as result cannot be binded to component
		 * (projects to delete project from list here)
		*/
		try {
			projects = await getProjectsRequest();
		} catch (e) {
			error = Error(e);
		}
	});
</script>

<div>
	{#if error}
		<p style="color: red">{error.message}</p>
	{:else if projects}
		{#each projects as project}
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
						<DeleteProject bind:projects={projects} {project} />
					</div>
				</div>
			</div>
		{/each}
	{:else}
		<div class="spinner-border" role="status" />
	{/if}
	<CreateProject />
</div>