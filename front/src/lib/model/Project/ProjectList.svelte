<script lang="ts">
	import { onMount } from 'svelte';
	import { getLastUpdate } from '$lib/utils';
	import DeleteProject from './DeleteProject.svelte';
	import type { Project } from '$lib/model/api/model/project';
	import ErrorComponent from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import ExportProject from './ExportProject.svelte';
	import { getProjectsRequest } from '$lib/model/api/project';
	import RenameProject from './RenameProject.svelte';
	import CreateProject from './CreateProject.svelte';

	let projects: Project[];
	let error: string;

	onMount(async () => {
		/**
		 * Cannot use svelte promise logic as result cannot be binded to component
		 * (projects to delete project from list here)
		 */
		try {
			projects = await getProjectsRequest();
		} catch (e: any) {
			error = e.message;
		}
	});
</script>

<div>
	{#if error}
		<ErrorComponent message={error} />
	{:else if projects}
		{#each projects as project}
			<div class="list-group-item list-group-item-action">
				<div class="row">
					<div class="col">
						<a id="redirect{project.id}" href="/project/{project.id}">
							<h5 class="mb-1">
								{project.name}
							</h5>
							<small>{getLastUpdate(project)}</small>
						</a>
					</div>

					<div class="col">
						<RenameProject bind:project />
						<DeleteProject bind:projects {project} />
						<ExportProject {project} />
					</div>
				</div>
			</div>
		{/each}
	{:else}
		<Spinner />
	{/if}
	<CreateProject />
</div>
