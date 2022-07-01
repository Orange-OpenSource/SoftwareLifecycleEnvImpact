<script>
	import { get } from '$lib/api';
	import ImpactByIndicator from './ImpactByIndicator.svelte';
	import ImpactBySubtask from './ImpactBySubtask.svelte';

	/*Bound var*/
	export let selectedTask;

	let impactByIndicator
	let impactBySubtask

	/*Trigger update when selected task is updated*/
	$: selectedTask, updateImpacts();

	async function updateImpacts() {
		if (selectedTask != undefined) {
			let res = await get('tasks/'+selectedTask.id+'/impacts')
			/*TODO: bad solution, why two requests ?*/
			if (res.status === 404) alert('No task found with this id' + selectedTask.id);
			else {
				impactByIndicator = res
			}

			res = await get('tasks/'+selectedTask.id+'/subtasksimpacts')
			if (res.status === 404) alert('No task found with this id' + selectedTask.id);
			else {
				impactBySubtask = res
			}
		}
	}
</script>

<ImpactByIndicator {impactByIndicator}/>
<ImpactBySubtask {impactBySubtask}/>