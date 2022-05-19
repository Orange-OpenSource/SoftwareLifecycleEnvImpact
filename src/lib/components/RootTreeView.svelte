<script lang="ts">
	import { getTasksFromModel } from '$lib/controllers/RequestController';
	import TreeView from './TreeView.svelte';
	import { createEventDispatcher, tick } from 'svelte';

	/* Bound var */
	export let modify: any;
	export let CURRENT_MODEL_ID: any;
	export let templates: any;
	export let myChart: any;

	let tasks: any[] = [];
	let rootTask, parent_task_id: any;
	let subtasks: never[] = [];

	const dispatch = createEventDispatcher();

	async function handleMessage(event: { detail: { text: any } }) {
		if (event.detail.text === 'updateTree') await updateTree();

		dispatch('message', {
			text: 'updateChart'
		});
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

	/**
	 * Update the treeview with the global "CURRENT_MODEL_ID" variable.
	 */
	export async function updateTree() {
		await tick();
		rootTask = await getTasksFromModel(CURRENT_MODEL_ID);
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
</script>

<div class="col scroll">
	<TreeView on:message={handleMessage} bind:templates bind:myChart bind:CURRENT_MODEL_ID {parent_task_id} {subtasks} bind:modify {tasks} />
</div>
