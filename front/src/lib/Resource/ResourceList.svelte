<script lang="ts">
	import AddResource from './AddResource.svelte';
	import DeleteResource from './DeleteResource.svelte';
	import Error from '$lib/Error.svelte';
	import ResourceInput from './ResourceInput.svelte';
	import type { Task } from '$lib/api/dataModel';

	/*Bound var*/
	export let task: Task;
	export let modify: boolean;

	let editResource = false;

	$: if (!modify) editResource = false;

	let error = '';
</script>

{#if error}
	<Error message={error} />
{/if}

<ul class="list-group list-group-flush list-group-numbered">
	{#if task.resources != null}
		{#each task.resources as resource}
			<li class="list-group-item d-flex p-1">
				<div class="ms-2">
					<div class="d-flex justify-content-between">
						<div class="fw-bold">{resource.name}</div>
						{#if modify}
							<div>
								<input on:click|stopPropagation={() => (editResource = !editResource)} type="image" src="/pencil.svg" width="25" height="25" alt="Pencil" loading="lazy" />
								<DeleteResource bind:task {resource} />
							</div>
						{/if}
					</div>
					<div class="ms-1">
						<ResourceInput bind:resource modify={editResource} />
					</div>
				</div>
			</li>
		{/each}
	{/if}
	{#if modify}
		<li class="list-group-item d-flex p-1">
			<div class="ms-2">
				<AddResource bind:task />
			</div>
		</li>
	{/if}
</ul>
