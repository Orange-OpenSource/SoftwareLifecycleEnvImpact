<script lang="ts">
	import { getTasksFromModel } from '$lib/controllers/RequestController';
	import Task from './Task.svelte';
	import Header from './Header.svelte';
	
	/*Bound vars*/
	export let selectedModel;
	export let selectedTask;

	let modify: boolean = false; // true if modifications are allowed (when "editing mode" is checked)
	let tasks: any[] = [];
	let rootTask, parent_task_id: any;
	let subtasks = [];

	/*Update tree when selected model is updated*/
	$: {
		if(selectedModel !== undefined){
			getTasksFromModel(selectedModel).then(
				res => rootTask = res
			).then(
				updateTree()
			)
		}
	}

	/**
	 * Put each task from one model into an array.
	 *
	 * @param array the array to put the tasks into.
	 */
	function pushEachTaskFromModelInArray(array: any) {
		for (let i = 0; i < array.length; i++) {
			tasks.push(array[i]);
			tasks = tasks;
			if (array[i].subtasks.length) {
				pushEachTaskFromModelInArray(array[i].subtasks);
			}
		}
	}
	
	function updateTree() {
		if(rootTask != undefined){
			tasks = [];
			tasks.push(rootTask);
			pushEachTaskFromModelInArray(rootTask.subtasks);
			tasks = tasks;

			parent_task_id = rootTask.id;
			subtasks = rootTask.subtasks;

			if (subtasks.length === 0) {
				modify = true;
			}
		}
	}

</script>

{#if selectedModel == undefined}
	No model selected
{:else}
	<Header bind:modify {selectedModel}/>
	<div class="col scroll">
		<Task bind:selectedTask bind:modify {selectedModel} {parent_task_id} {subtasks}{tasks} />
	</div>
{/if}

