<script lang="ts">
	import ImpactByIndicator from './ImpactByIndicator.svelte';
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

{#if selectedTask != undefined}
	{#await impactPromise}
		<Spinner />
	{:then impact}
		{#if impact != undefined}
			<ImpactByIndicator environmentalImpact={impact.task_impact} />

			<h5>Subtask</h5>
			<ImpactBySubtask bind:selectedTask impactBySubtask={impact.subtasks} />

			<h5>Resources</h5>
			<ImpactByResource impactByResource={impact.resources} />
		{/if}
	{:catch error}
		<Error message={error.message} />
	{/await}
{:else}
	No task selected
{/if}
