<script>
	import { get } from '$lib/api';
	import ImpactByIndicator from './ImpactByIndicator.svelte';
	import ImpactBySubtask from './ImpactBySubtask.svelte';
	import ImpactByResource from './ImpactByResource.svelte';

	/*Bound var*/
	export let selectedTask;

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
				console.log('res')
				console.log(res)
				impactByIndicator = res.task_impact
				impactBySubtask = res.subtasks
				impactByResource = res.resources.impacts
			}
		}
	}
</script>


<h5>By indicator</h5>
<ImpactByIndicator {impactByIndicator}/>

<h5>By subtask</h5>
<ImpactBySubtask {impactBySubtask}/>

<h5>By resource</h5>
<ImpactByResource {impactByResource}/>