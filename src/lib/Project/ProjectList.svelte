<script>
	import CreateProject from '$lib/Project/CreateProject.svelte';
	import RenameProject from '$lib/Project/RenameProject.svelte';
	import { getLastUpdate } from '$lib/utils';
	import { get } from '$lib/api';
	import DeleteProject from './DeleteProject.svelte';
	import { onMount } from 'svelte';

	let projects
	let error

	onMount(async () => {
		const res = await get('projects')
		switch (res.status) {
            case undefined:
                projects = res
				break;
            case 404:
				error =  new Error('Cannot retrieve projects')
            default:
				error = new Error(res.status + ' error')
        }
  });
</script>

<div>
	{#if error}
		<p style="color: red">{error.message}</p>
	{:else if projects}
		<ul class="list-group list-group-flush">
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
							<DeleteProject bind:projects {project} />
						</div>
					</div>
				</div>
			{/each}
		</ul>
	{:else}
		<div class="spinner-border" role="status"/>
	{/if}

	<CreateProject />
</div>
