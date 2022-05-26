<script>
	import { page } from '$app/stores';
	import { onMount, tick } from 'svelte';
	import TaskTree from '$lib/TaskTree/TaskTree.svelte';
	import ModelList from '$lib/Model/ModelList.svelte';
	import Impact from '$lib/Impact/Impact.svelte';
	import { get } from '$lib/api';
	import Split from 'split.js';

	let projectId = $page.params.id; // id of project clicked on (arg in URL "/project/X")

	let selectedModel;
	let selectedTask;
	let models = [];

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


	onMount(async function () {
		if (document.querySelector('div.modal-backdrop.fade.show')) document.querySelector('div.modal-backdrop.fade.show').remove();

		const res = await get('projects/'+projectId+'/models')
		if (res.status === '404') alert('No project found with this id');
		else{
			models = res
			selectedModel = models[0];
			selectedTask = selectedModel.rootTask;
			updateSplit()
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
