<script lang="ts">
	import { getTasksFromModel } from '../controllers/RequestController';
	import TreeView from './TreeView.svelte';
	import { tick } from 'svelte';

	export let modify: any;
	export let model_id: any;

	let rootTask, parent_task_id: any;
	let subtasks: never[] = [];

	async function handleMessage(event: { detail: { text: any } }) {
		await updateTree();
	}

	export async function updateTree() {
		await tick();
		rootTask = await getTasksFromModel(model_id);
		parent_task_id = rootTask.id;
		subtasks = rootTask.subtasks;
	}
</script>

<div class="col scroll">
	<TreeView on:message={handleMessage} bind:model_id {parent_task_id} {subtasks} {modify} />
</div>
