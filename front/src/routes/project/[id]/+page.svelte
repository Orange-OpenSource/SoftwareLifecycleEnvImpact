<script lang="ts">
	import { page } from '$app/stores';
	import TaskTree from '$lib/model/TaskTree/TaskTree.svelte';
	import ModelList from '$lib/model/Model/ModelList.svelte';
	import Impact from '$lib/model/Impact/Impact.svelte';
	import Split from 'split.js';
	import { onMount } from 'svelte';
	import type { Task } from '$lib/model/api/model/task';
	import type { Model } from '$lib/model/api/model/model';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import ModelComparison from '$lib/model/Model/Comparison/ModelsComparison.svelte';
	import { getProjectRequest } from '$lib/model/api/project';

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
			<div class="sticky-top">
				<ModelList bind:selectedModel bind:selectedModels bind:compareModels {project} />
			</div>
		{:catch error}
			<Error message={error.message} slot="error" />
		{/await}
	</div>

	{#if !compareModels}
		<div id="split-1">
			<div class="col">
				<h2 class="title">Tasks</h2>
				<TaskTree bind:selectedTask {selectedModel} />
			</div>
		</div>

		<div id="split-2">
			<div class="col sticky-top">
				<h2 class="title">Impact</h2>
				<Impact bind:selectedTask />
			</div>
		</div>
	{:else}
		<div id="split-1">
			<div class="col">
				<h2 class="title">Compare</h2>
				<ModelComparison models={selectedModels} />
			</div>
		</div>
	{/if}
</div>
