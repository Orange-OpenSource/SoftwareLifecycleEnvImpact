<script lang="ts">
	import { updateResourceRequest } from '$lib/api/resource';
	import type { Resource } from 'src/model/resource';
	import type { Task } from 'src/model/task';
	import AddResource from './AddResource.svelte';
	import DeleteResource from './DeleteResource.svelte';

	/*Bound var*/
	export let task: Task;
	export let modify: boolean;

	let error = '';

	async function updateResource(resource: Resource) {
		await updateResourceRequest(resource, String(resource.value));
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
			{#if modify}
				{#if error != ''}
					<p style="color: red">{error}</p>
				{/if}
				{#if resource == task.resources[task.resources.length - 1]}
					<li class="list-group-item d-flex align-items-center flex-row-reverse">
						<AddResource bind:task />
					</li>
				{/if}
			{/if}
		{/each}
	</ul>
{/if}
