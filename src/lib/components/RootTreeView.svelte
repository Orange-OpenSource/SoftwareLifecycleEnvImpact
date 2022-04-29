<script lang="ts">
	import { getTasksFromModel } from '../controllers/RequestController';
	import TreeView from './TreeView.svelte';
	import { tick } from 'svelte';

	export let modify: any;
	export let model_id: any;

	let rootTask;
	let subtasks = [];

	export async function updateTree() {
		await tick();
		rootTask = await getTasksFromModel(model_id);
		subtasks = rootTask.subtasks;
	}
</script>

<div class="col scroll">
	<TreeView {subtasks} {modify} />
</div>
