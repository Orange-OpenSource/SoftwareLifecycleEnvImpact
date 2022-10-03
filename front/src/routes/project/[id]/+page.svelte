<script lang="ts">
	import { page } from '$app/stores';
	import TaskTree from '$lib/TaskTree/TaskTree.svelte';
	import ModelList from '$lib/Model/ModelList.svelte';
	import Impact from '$lib/Impact/Impact.svelte';
	import Split from 'split.js';
	import { onMount } from 'svelte';
	import type { Task } from 'src/model/task';
	import type { Model } from 'src/model/model';
	import type { Project } from 'src/model/project';
	import { getProjectRequest } from '$lib/api/project';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import ModelComparison from '$lib/Model/Comparison/ModelsComparison.svelte';

	let projectId = $page.params.id; // id of project clicked on (arg in URL "/project/X")

	let projectPromise = getProjectRequest(+projectId).then((res) => {
		if (res.models != null) {
			selectedModel = res.models[0];
		}
		return res;
	});

	let selectedModel: Model;
	let selectedModels: Model[] = [];
	let selectedTask: Task;

	let split: Split.Instance;

	let compareModels = false;

	$: selectedModel, updateSelectedTask();

	$: selectedModels, updateComparison();

	$: compareModels,
		() => {
			/*Update screen layout to two or three columns if comparison is activated*/
			if (compareModels) setTwoColumnsSplit();
			else setThreeColumnsSplit();
		};

	function updateComparison() {
		/*Deactivate model comparison if less than two are selected*/
		if (selectedModels.length < 2) compareModels = false;
	}

	function updateSelectedTask() {
		/*Select a model root task as selected task to display the complete model impacts*/
		if (selectedModel != undefined) {
			selectedTask = selectedModel.root_task;
		}
	}

	function setTwoColumnsSplit() {
		if (split) split.destroy();
		split = Split(['#split-0', '#split-1'], {
			sizes: [25, 75],
			minSize: 0,
			snapOffset: 150
		});
	}

	async function setThreeColumnsSplit() {
		if (split) split.destroy();
		split = Split(['#split-0', '#split-1', '#split-2'], {
			sizes: [25, 50, 25],
			minSize: 0,
			snapOffset: 150,
			onDrag: function () {
				for (let i = 0; i < 3; i++) {
					let element = document.getElementById('split-' + i);
					if (element != null) {
						if (element.offsetWidth === 0) {
							element.style.visibility = 'hidden';
						} else {
							element.style.visibility = 'visible';
						}
					}
				}
			}
		});
		return;
	}

	function compareModelsButton() {
		compareModels = true;
		setTwoColumnsSplit();
	}

	onMount(async () => {
		setThreeColumnsSplit();
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

<div class="split">
	<div id="split-0">
		<h2 class="title">My models</h2>
		{#await projectPromise}
			<Spinner />
		{:then project}
			<ModelList bind:selectedModel bind:selectedModels {project} />
			{#if selectedModels.length > 1}
				<button on:click|stopPropagation={compareModelsButton} type="button" class="col-5 btn btn-light">Compare</button>
			{/if}
		{:catch error}
			<Error message={error.message} slot="error" />
		{/await}
	</div>

	{#if !compareModels}
		<div id="split-1">
			<h2 class="title">Tasks</h2>
			<TaskTree bind:selectedTask {selectedModel} />
		</div>

		<div id="split-2">
			<div class="sticky-top">
				<h2 class="title">Impact</h2>
				<Impact bind:selectedTask />
			</div>
		</div>
	{:else}
		<div id="split-1">
			<h2 class="title">Compare</h2>
			<ModelComparison models={selectedModels} />
		</div>
	{/if}
</div>
