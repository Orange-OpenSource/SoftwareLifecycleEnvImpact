<script lang="ts">
	import ImpactBySubtask from './ImpactBySubtask.svelte';
	import ImpactByResource from './ImpactByResource.svelte';
	import { getTaskImpact } from '$lib/api/task';
	import type { TaskImpact, Task } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';

	/*Bound var*/
	export let selectedTask: Task;
	let olderTask: Task;

	let impactPromise: Promise<TaskImpact>;

	/*Trigger update when selected task is updated*/
	$: selectedTask, updateImpacts();

	function updateImpacts() {
		// WIthout this, sometimes the selectedTask refresh was called indefinitely
		if (selectedTask != undefined && (olderTask == undefined || olderTask != selectedTask)) {
			olderTask = selectedTask;
			impactPromise = getTaskImpact(selectedTask);
		}
	}
</script>

<div class="col">
	{#if selectedTask != undefined}
		{#await impactPromise}
			<Spinner />
		{:then impact}
			{#if impact != undefined}
				<div class="row">
					<h1>{selectedTask.name}</h1>
				</div>
				{#if impact.subtasks.length > 0}
					<div class="row">
						<h3>Tasks:</h3>
					</div>
					<div class="row">
						<ImpactBySubtask bind:selectedTask impactBySubtask={impact.subtasks} />
					</div>
				{/if}
				<div class="row">
					<h3>Resources:</h3>
				</div>
				<div class="row">
					<ImpactByResource impactByResource={impact.resources} />
				</div>
			{/if}
		{:catch error}
			<Error message={error.message} />
		{/await}
	{:else}
		No element selected
	{/if}
</div>
