<script lang="ts">
	import Header from './Header.svelte';
	import { getModelTasksRequest } from '$lib/api/model';
	import TaskComponent from '$lib/Task/Task.svelte';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import type { Model, Task } from '$lib/api/dataModel';

	/*Bound vars*/
	export let selectedModel: Model;
	export let selectedTask: Task;

	let modify = false; // true if modifications are allowed (when "editing mode" is checked)
	let rootTaskPromise: Promise<Task>;

	/*Trigger update when selected model is updated*/
	$: selectedModel, updateTree();

	async function updateTree() {
		modify = false;
		if (selectedModel != undefined) {
			rootTaskPromise = getModelTasksRequest(selectedModel.id).then((res) => {
				/* Switch on modify if ther is no task in the model*/
				if (res.subtasks.length === 0) {
					modify = true;
				}
				return res;
			});
		}
	}
</script>

{#await rootTaskPromise}
	<Spinner />
{:then rootTask}
	{#if selectedModel == undefined}
		No model selected
	{:else if rootTask != undefined}
		<Header bind:modify bind:selectedTask {selectedModel} />
		<div class="col scroll">
			<TaskComponent task={rootTask} bind:selectedTask {modify} {selectedModel} parentTask={rootTask} />
		</div>
	{/if}
{:catch error}
	<Error message={error.message} />
{/await}
