<script>
	import { page } from '$app/stores';
	import TaskTree from '$lib/TaskTree/TaskTree.svelte';
	import ModelList from '$lib/Model/ModelList.svelte';
	import Impact from '$lib/Impact/Impact.svelte';
	import { get } from '$lib/api';
	import Split from 'split.js';
import { onMount } from 'svelte';

	let projectId = $page.params.id; // id of project clicked on (arg in URL "/project/X")

	let project = retrieveProject();

	let selectedModel;
	let selectedTask;

	$: selectedModel, updateSelectedTask()

	function updateSelectedTask(){
		/*Select a model root task as selected task to display the complete model impacts*/
		if(selectedModel != undefined){
			selectedTask = selectedModel.root_task;
		}
	}

	function updateSplit(){
		Split(['#split-0', '#split-1', '#split-2'], {
			sizes: [25, 50, 25],
			minSize: 0,
			snapOffset: 150,
			onDrag: function () {
				for (let i = 0; i < 3; i++) {
					let element = document.getElementById('split-' + i);
					if (element.offsetWidth === 0) {
						element.style.visibility = 'hidden';
					} else {
						element.style.visibility = 'visible';
					}
				}
			}
		})
	}

	async function retrieveProject() {
		const res = await get('projects/'+projectId)

		switch (res.status) {
			case undefined:
				project = res
				selectedModel = project.models[0];
				updateSplit()
				break;
			case 404:
				throw new Error('No project found with this id')
			default:
				throw new Error(res.status + ' error')
		}
	}

	onMount(async function () {
		if (document.querySelector('div.modal-backdrop.fade.show')) document.querySelector('div.modal-backdrop.fade.show').remove();
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

<div class="split">
	{#await project}
		<div class="spinner-border" role="status"/>
	{:then}
		<div id="split-0">
			<h2 class="title">My models</h2>
			<ModelList bind:selectedModel bind:project />
		</div>

		<div id="split-1">
			<h2 class="title">Tasks</h2>
			<TaskTree bind:selectedTask {selectedModel} />
		</div>

		<div id="split-2">
			<h2 class="title">Impact</h2>
			<Impact bind:selectedTask />
		</div>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</div>
