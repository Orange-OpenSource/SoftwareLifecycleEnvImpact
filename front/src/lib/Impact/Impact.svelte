<script lang="ts">
	import ImpactBySubtask from './ImpactBySubtask.svelte';
	import ImpactBySource from './ImpactBySource.svelte';
	import { getTaskImpact } from '$lib/api/task';
	import type { TaskImpact, Task } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';

	/*Bound var*/
	export let selectedTask: Task;
	let olderTask: Task;

	let impactPromise: Promise<TaskImpact>;
	let selectedImpactName = 'Climate change';

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
			{#if impact != undefined && Object.keys(impact.impact_sources).length}
				<div class="row">
					<h1 class="text-primary">{selectedTask.name}</h1>
				</div>
				<div class="row">
					<select class="form-select" bind:value={selectedImpactName} required>
						{#each Object.entries(impact.total) as [key, _]}
							<option value={key} class="form-check-input">{key}</option>
						{/each}
					</select>
				</div>
				{#if impact.sub_tasks.length > 0}
					<!-- <div class="row">
						<h3>Tasks:</h3>
					</div> -->
					<div class="row">
						<ImpactBySubtask bind:selectedTask impactBySubtask={impact.sub_tasks} {selectedImpactName} />
					</div>
				{/if}
				<div class="row">
					<ImpactBySource impactBySource={impact.impact_sources} />
				</div>
			{:else}
				No impact
			{/if}
		{:catch error}
			<Error message={error.message} />
		{/await}
	{:else}
		No element selected
	{/if}
</div>
