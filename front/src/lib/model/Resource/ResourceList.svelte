<script lang="ts">
	import { updateResourceRequest } from '$lib/model/api/resource';
	import type { Resource } from '$lib/model/api/model/resource';
	import type { Task } from '$lib/model/api/model/task';
	import AddResource from './AddResource.svelte';
	import DeleteResource from './DeleteResource.svelte';
	import Error from '$lib/Error.svelte';

	/*Bound var*/
	export let task: Task;
	export let modify: boolean;

	let error = '';

	async function updateResource(resource: Resource) {
		try {
			await updateResourceRequest(resource, String(resource.value));
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

{#if task.resources != null}
	<ul class="list-group list-group-flush">
		{#each task.resources as resource}
			<li class="list-group-item">
				<div class="d-flex w-100 justify-content-between align-items-center">
					<div>
						<label class="input-group-text" for="typeNumber">{resource.name}</label>
						<input
							type="number"
							id="typeNumber{resource.id}"
							class="form-control"
							readonly={!modify}
							bind:value={resource.value}
							min="0"
							on:change={() => updateResource(resource)}
							on:click={() => {}}
						/>
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
