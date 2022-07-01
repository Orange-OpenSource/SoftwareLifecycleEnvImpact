<script>
	import Header from './Header.svelte';
	import { get } from '$lib/api';
	import Task from '../Task/Task.svelte';

	/*Bound vars*/
	export let selectedModel;
	export let selectedTask;

	let modify = false; // true if modifications are allowed (when "editing mode" is checked)
	let rootTask;
	let taskTemplates = retrieveTaskTemplates();
	let error = ''

	/*Trigger update when selected model is updated*/
	$: selectedModel, updateTree();

	async function updateTree() {
		modify=false;
		if(selectedModel != undefined){
			const res = await get('models/'+selectedModel.id+'/tasks')

			error = '' 
			switch (res.status) {
				case undefined:
				rootTask = res
				/* Switch on modify if ther is no task in the model*/
				if (rootTask.subtasks.length === 0) {
					modify = true;
				}
					break;
				case 404:
					error = 'No model found with this id' + selectedModel.id
					break;
				default:
					error = res.status + ' error'
					break;
			}
		}
	}

	async function retrieveTaskTemplates(){
		const res = await get('tasktemplates')
		switch (res.status) {
			case undefined:
				taskTemplates = res
				break;
			case 404:
				throw new Error('Cannot retrieve task templates' + selectedModel.id)
			default:
				throw new Error(res.status + ' error')
		}
	}
</script>

<div class="col">
	{#await taskTemplates}
		<div class="spinner-border" role="status"/>
	{:then}
		{#if error != ''}
			<p style="color: red">{error}</p>
		{/if}
		{#if selectedModel == undefined}
			No model selected
		{:else if rootTask != undefined}
			<Header bind:modify {selectedModel} />
			<div class="col scroll">
				<Task bind:task={rootTask} bind:selectedTask {modify} {selectedModel} parentTask={rootTask} {taskTemplates}/>
			</div>
		{/if}
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</div>