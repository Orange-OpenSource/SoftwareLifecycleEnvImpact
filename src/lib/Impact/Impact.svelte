<script>
	import { get } from '$lib/api';
	import ImpactByIndicator from './ImpactByIndicator.svelte';
	import ImpactBySubtask from './ImpactBySubtask.svelte';
	import ImpactByResource from './ImpactByResource.svelte';

	/*Bound var*/
	export let selectedTask = undefined;

	let impactByIndicator
	let impactBySubtask
	let impactByResource

	/*Trigger update when selected task is updated*/
	$: selectedTask, updateImpacts();

	async function updateImpacts() {
		if (selectedTask != undefined) {
			let res = await get('tasks/'+selectedTask.id+'/impacts')
			if (res.status === 404) alert('No task found with this id' + selectedTask.id);
			else {
				impactByIndicator = res.task_impact
				impactBySubtask = res.subtasks
				impactByResource = res.resources
			}
		}
	}
</script>

<ImpactByIndicator {impactByIndicator}/>

{#if selectedTask != undefined && selectedTask.subtasks.length != 0}
	<h5>Subtask</h5>
	<ImpactBySubtask bind:selectedTask {impactBySubtask}/>
{/if}

<h5>Resources</h5>
<ImpactByResource {impactByResource}/>