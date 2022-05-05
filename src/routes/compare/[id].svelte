<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { getModels, getModelInformations } from '$lib/controllers/RequestController';
	import { checkIfLogged } from '$lib/controllers/LoginController';
	import Split from 'split.js';
	import { browser } from '$app/env';
	import { goto } from '$app/navigation';

	checkIfLogged();

	let idProject = $page.params.id;
	let models: string | any[] = [];
	let modelsContent: any = [];

	/**
	 * Load all the models.
	 */
	async function loadModels() {
		models = await getModels(idProject);
		modelsContent = [];
		for (var i = 0; i < models.length; i++) {
			let content = await getModelInformations(models[i].id);
			modelsContent.push(content);
		}
		modelsContent = modelsContent;
	}

	function goBack() {
		if (browser) {
			goto('/view/' + idProject);
		}
	}

	onMount(async function () {
		await loadModels();

		Split(['#split-0', '#split-1'], {
			sizes: [25, 75],
			minSize: 0,
			snapOffset: 150,
			onDrag: function () {
				for (let i = 0; i < 2; i++) {
					let element = document.getElementById('split-' + i);
					if (element!.offsetWidth === 0) {
						element!.style.visibility = 'hidden';
					} else {
						element!.style.visibility = 'visible';
					}
				}
			}
		});
	});
</script>

<svelte:head>
	<title>Compare models</title>
</svelte:head>

<div class="split">
	<div id="split-0">
		<button on:click={goBack} type="button" class="col btn btn-outline-primary" style="margin-top: 20px;">Go back to editing</button>

		<h2 class="title">My models</h2>

		<ul class="list-group list-group-flush" style="margin-bottom : 5px;">
			{#each modelsContent as model}
				<li class="list-group-item">
					<div class="card-body d-flex justify-content-between">
						<span>{model.name}</span>
						<div>
							<input type="checkbox" class="modelsInput" name={model.id} />
						</div>
					</div>
				</li>
			{/each}
		</ul>
	</div>

	<div id="split-1">
		<h2 class="title">Differences</h2>
	</div>
</div>
