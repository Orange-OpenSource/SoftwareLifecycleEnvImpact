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
	import Error from '$lib/Error.svelte'

	let projectId = $page.params.id; // id of project clicked on (arg in URL "/project/X")

	let projectPromise: Promise<Project>;

	let selectedModel: Model;
	let selectedTask: Task;

	$: selectedModel, updateSelectedTask();
	$: projectPromise, updateSplit(); /*Mandatory to redraw splitjs, do not work in an async context*/

	function updateSelectedTask() {
		/*Select a model root task as selected task to display the complete model impacts*/
		if (selectedModel != undefined) {
			selectedTask = selectedModel.root_task;
		}
	}

	function updateSplit() {
		Split(['#split-0', '#split-1', '#split-2'], {
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
	}

	async function retrieveProject() {
		projectPromise = getProjectRequest(projectId).then((res) => {
			if (res.models != null) {
				selectedModel = res.models[0];
			}
			return res;
		});
	}

	onMount(async function () {
		retrieveProject();
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

{#await projectPromise}
	<div class="spinner-border" role="status" />
{:then project}
	<div class="split">
		<div id="split-0">
			<h2 class="title">My models</h2>
			<ModelList bind:selectedModel {project} />
		</div>

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
	</div>
{:catch error}
	<Error message={error.message}/>
{/await}
