<script>
	import Task from './Task/Task.svelte';
	import Header from './Header.svelte';
	import { get } from '$lib/api';

	/*Bound vars*/
	export let selectedModel;
	export let selectedTask;

	let modify = false; // true if modifications are allowed (when "editing mode" is checked)
	let rootTask;

	/*Trigger update when selected model is updated*/
	$: selectedModel, updateTree();

	async function updateTree() {
		if(selectedModel != undefined){
			const res = await get('models/'+selectedModel.id+'/tasks')

			if (res.status === 404) alert('No model found with this id' + selectedModel.id);
			else {
				rootTask = res
				/* Switch on modify if ther is no task in the model*/
				if (rootTask.subtasks.length === 0) {
					modify = true;
				}
			}
		}
	}
</script>

<div class="col">
	{#if selectedModel == undefined}
	No model selected
{:else if rootTask != undefined}
	<Header bind:modify {selectedModel} />
	<div class="col scroll">
		<Task bind:task={rootTask} bind:selectedTask {modify} {selectedModel} parentTaskId={rootTask.id}/>
	</div>
{/if}
</div>