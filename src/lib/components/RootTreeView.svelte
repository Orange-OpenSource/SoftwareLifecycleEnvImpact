<script lang="ts">
	import { getTasksFromModel } from '../controllers/RequestController';
	import TreeView from './TreeView.svelte';
	import { tick } from 'svelte';

	export let modify: any;
	export let model_id: any;
	let tasks: any[] = [];
	let rootTask, parent_task_id: any;
	let subtasks: never[] = [];

	async function handleMessage(event: { detail: { text: any } }) {
		await updateTree();
	}

	function pushEachTaskFromModelInArray(array: any) {
		for (let i = 0; i < array.length; i++) {
			tasks.push(array[i]);
			tasks = tasks;
			if (array[i].subtasks.length){
				pushEachTaskFromModelInArray(array[i].subtasks);
			}
		}
	}

	export async function updateTree() {
		await tick();
		rootTask = await getTasksFromModel(model_id);

		tasks = [];
		tasks.push(rootTask);
		pushEachTaskFromModelInArray(rootTask.subtasks);
		tasks = tasks;

		parent_task_id = rootTask.id;
		subtasks = rootTask.subtasks;
	}
</script>

<div class="col scroll">
	<TreeView on:message={handleMessage} bind:model_id {parent_task_id} {subtasks} {modify} {tasks}/>
</div>
