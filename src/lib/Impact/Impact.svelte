<script lang="ts">
	import ImpactByIndicator from './ImpactByIndicator.svelte';
	import ImpactBySubtask from './ImpactBySubtask.svelte';
	import ImpactByResource from './ImpactByResource.svelte';
	import type { Task } from 'src/model/task';
	import { getTaskImpact } from '$lib/api/task';
	import type { TaskImpact } from 'src/model/impacts';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';

	/*Bound var*/
	export let selectedTask: Task;

	let impactPromise: Promise<TaskImpact>;

	/*Trigger update when selected task is updated*/
	$: selectedTask, updateImpacts();

	async function updateImpacts() {
		if (selectedTask != undefined) {
			impactPromise = getTaskImpact(selectedTask).then();
		}
	}
</script>

{#await impactPromise}
	<Spinner />
{:then impact}
	{#if impact != undefined}
		<ImpactByIndicator impact={impact.task_impact} />

		{#if selectedTask != undefined && selectedTask.subtasks.length != 0}
			<h5>Subtask</h5>
			<ImpactBySubtask {selectedTask} impactBySubtask={impact.subtasks} />
		{/if}

		<h5>Resources</h5>
		<ImpactByResource impactByResource={impact.resources} />
	{/if}
{:catch error}
	<Error message={error.message} />
{/await}
