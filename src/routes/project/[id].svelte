<script>
	import { page } from '$app/stores';
	import { onMount, tick } from 'svelte';
	import TaskTree from '$lib/TaskTree/TaskTree.svelte';
	import ModelList from '$lib/Model/ModelList.svelte';
	import Impact from '$lib/Impact/Impact.svelte';
	import { get2RowsSplitObject, get3RowsSplitObject } from '$lib/utils';
import { get } from '$lib/api';

	let projectId = $page.params.id; // id of project clicked on (arg in URL "/project/X")

	let selectedModel;
	let selectedTask;
	let models = [];

	/*TODO remove*/
	let splitjs; // Splitjs object

	/**
	 * Switch to comparaison screen or goes back to initial screen
	 */
	async function comparePage() {
		if (!compare_screen) {
			splitjs.destroy();
			compare_screen = true;
			await tick();
			splitjs = get2RowsSplitObject(document);
		} else {
			splitjs.destroy();
			compare_screen = false;
			await tick();
			splitjs = get3RowsSplitObject(document);

			ctx = document.getElementById('myChart').getContext('2d');
			myChart = getChart(ctx, labels, data);
			await rootTreeView.updateTree();
		}
	}

	onMount(async function () {
		if (document.querySelector('div.modal-backdrop.fade.show')) document.querySelector('div.modal-backdrop.fade.show').remove();

		const res = await get('projects/'+projectId+'/models')
		if (res.status === '404') alert('No project found with this id');
		else{
			models = res
			selectedModel = models[0];
			selectedTask = selectedModel.rootTask;
			splitjs = get3RowsSplitObject(document);
		}
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

<div class="split">
	<div id="split-0">
		<h2 class="title">My models</h2>

		<ModelList {models} {projectId} bind:selectedModel />

		<div class="row d-flex justify-content-evenly">
			<!--
			<svelte:component this={ModalCreationModel} bind:CURRENT_MODEL_ID bind:CURRENT_MODEL_NAME bind:rootTreeView bind:modify bind:idProject bind:models />
			<button on:click={comparePage} type="button" class="col-5 btn btn-outline-primary">Compare models</button>
			-->
		</div>
	</div>

	<div id="split-1">
		<h2 class="title">Tasks</h2>
		<TaskTree bind:selectedTask {selectedModel} />
	</div>

	<div id="split-2">
		<h2 class="title">Impact</h2>
		<Impact {selectedTask} />
	</div>
</div>
