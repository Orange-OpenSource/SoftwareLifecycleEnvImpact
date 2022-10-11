<script lang="ts">
	import type { Task } from '$lib/model/api/model/task';
	import AddResource from './AddResource.svelte';
	import DeleteResource from './DeleteResource.svelte';
	import Error from '$lib/Error.svelte';
	import ResourceInput from './ResourceInput.svelte';

	/*Bound var*/
	export let task: Task;
	export let modify: boolean;

	let error = '';

	// async function updateResource(resource: Resource) {
	// 	try {
	// 		await updateResourceRequest(resource, String(resource.value));
	// 	} catch (e: any) {
	// 		error = e.message;
	// 	}
	// } TODO request to rename task
</script>

{#if task.resources != null}
	<ul class="list-group list-group-flush">
		{#each task.resources as resource}
			<li class="list-group-item">
				<div class="d-flex w-100 justify-content-between align-items-center">
					<div>
						<label class="input-group-text" for="typeNumber">{resource.name}</label>
						<ResourceInput bind:resourceInput={resource.input} {modify} />
					</div>

					{#if modify}
						<DeleteResource bind:task {resource} />
					{/if}
				</div>
			</li>
		{/each}
	</ul>
{/if}
{#if modify}
	{#if error}
		<Error message={error} />
	{/if}
	<li class="list-group-item d-flex align-items-center flex-row-reverse">
		<AddResource bind:task />
	</li>
{/if}
