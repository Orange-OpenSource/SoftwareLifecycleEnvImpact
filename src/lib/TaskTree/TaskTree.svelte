<script>
	import Task from './Task/Task.svelte';
	import Header from './Header.svelte';
	import { get } from '$lib/api';
	import { onMount } from 'svelte';

	/*Bound vars*/
	export let selectedModel;
	export let selectedTask;

	let modify = false; // true if modifications are allowed (when "editing mode" is checked)
	let rootTask;
	let taskTemplates;

	/*Trigger update when selected model is updated*/
	$: selectedModel, updateTree();

	async function updateTree() {
		modify=false;
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

	onMount(async function () {
		const res = await get('tasktemplates')
		if (res.status === 404) alert('Cannot retrieve task templates' + selectedModel.id);
		else{
			taskTemplates = res
		}
	});
</script>

<div class="col">
	{#if selectedModel == undefined}
	No model selected
{:else if rootTask != undefined}
	<Header bind:modify {selectedModel} />
	<div class="col scroll">
		<Task bind:task={rootTask} bind:selectedTask {modify} {selectedModel} parentTask={rootTask} {taskTemplates}/>
	</div>
{/if}
</div>