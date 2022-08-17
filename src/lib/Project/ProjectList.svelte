<script lang="ts">
	import { onMount } from 'svelte';
	import { getProjectsRequest } from '$lib/api/project';
	import CreateProject from '$lib/Project/CreateProject.svelte';
	import RenameProject from '$lib/Project/RenameProject.svelte';
	import { getLastUpdate } from '$lib/utils';
	import DeleteProject from './DeleteProject.svelte';
	import type { Project } from 'src/model/project';
	import ErrorComponent from '$lib/Error.svelte'
import Spinner from '$lib/Spinner.svelte';

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
		<ErrorComponent message={error}/>
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
		<Spinner/>
	{/if}
	<CreateProject />
</div>