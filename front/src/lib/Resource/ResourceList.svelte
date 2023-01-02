<script lang="ts">
	import AddResource from './AddResource.svelte';
	import DeleteResource from './DeleteResource.svelte';
	import Error from '$lib/Error.svelte';
	import ResourceInput from './ResourceInput.svelte';
	import type { Task } from '$lib/api/dataModel';

	/*Bound var*/
	export let task: Task;
	export let modify: boolean;

	let error = '';
</script>

{#if error}
	<Error message={error} />
{/if}
<ul class="list-group list-group-flush list-group-numbered ml-1">
	{#if task.resources != null}
		{#each task.resources as resource}
			<li class="list-group-item d-flex p-0">
				<div class="ms-2">
					<div class="row justify-content-start">
						<div class="fw-bold col-md-auto">{resource.name}</div>
						{#if modify}
							<div class="col">
								<DeleteResource bind:task {resource} />
							</div>
						{/if}
					</div>
					<div class="row ms-2">
						<ResourceInput bind:resource {modify} />
					</div>
				</div>
			</li>
		{/each}
	{/if}
	{#if modify}
		<li class="list-group-item p-0">
			<AddResource bind:task />
		</li>
	{/if}
</ul>
