<script lang="ts">
	import ImpactBySubtask from './ImpactBySubtask.svelte';
	import ImpactBySource from './ImpactBySource.svelte';
	import { getTaskImpact } from '$lib/api/task';
	import type { TaskImpact, Task } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import ImpactComplete from './ImpactComplete.svelte';

	/*Bound var*/
	export let selectedTask: Task;
	let olderTask: Task;

	let impactPromise: Promise<TaskImpact>;
	export let selectedImpactCategory = 'Climate change';
	export let showImpactCategorySelector = true;

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

<div class="col-md-auto">
	{#if selectedTask != undefined}
		{#await impactPromise}
			<Spinner />
		{:then impact}
			{#if impact != undefined && Object.keys(impact.impact_sources).length}
				<div class="row">
					<h1 class="text-primary">{selectedTask.name}</h1>
				</div>
				{#if showImpactCategorySelector}
					<div class="d-flex">
						<select class="form-select" bind:value={selectedImpactCategory} required>
							{#each Object.entries(impact.total) as [key, _]}
								<option value={key} class="form-check-input">{key}</option>
							{/each}
						</select>
					</div>
				{/if}
				{#if impact.sub_tasks.length > 0}
					<div class="row">
						<ImpactComplete bind:selectedTask {impact} {selectedImpactCategory} />
					</div>
					<div class="row">
						<ImpactBySubtask bind:selectedTask {impact} {selectedImpactCategory} />
					</div>
				{/if}
				<div class="row">
					<ImpactBySource bind:selectedTask {impact} {selectedImpactCategory} />
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
