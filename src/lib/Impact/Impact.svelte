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

	async function updateChart2() {
		/*Display the model impact*/
		if(selectedTask.parent_task_id == null){

		}else{ /*Display only the task impact*/
			
		}
	}

	async function updateImpacts() {
		if (selectedTask != undefined) {
			const res = await get('tasks/'+selectedTask.id+'/impacts')

			if (res.status === 404) alert('No task found with this id' + selectedTask.id);
			else {
				impactByIndicator = res

				const res2 = await get('tasks/'+selectedTask.id+'/subtasksimpacts')

				if (res2.status === 404) alert('No task found with this id' + selectedTask.id);
				else {
					impactBySubtask = res2
				}/*TODO very ugly*/
			}
		}
	}
	


</script>

<ImpactByIndicator {impactByIndicator}/>
<ImpactBySubtask {impactBySubtask}/>


