<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { getModels, getModelInformations, deleteModel } from '$lib/controllers/RequestController';
	import RootTreeView from '$lib/components/RootTreeView.svelte';
	import HeaderButtonsModel from '$lib/components/HeaderButtonsModel.svelte';
	import { checkIfLogged } from '$lib/controllers/LoginController';
	import ModalCreationModel from '$lib/components/modals/ModalCreationModel.svelte';
	import Split from 'split.js';
	import { browser } from '$app/env';
	import { goto } from '$app/navigation';

	checkIfLogged();

	let idProject = $page.params.id;
	let models: string | any[] = [];
	let modelsContent: any = [];
	let modify = false;
	let model_id: any;
	let rootTreeView: any;
	let model_name: string;

	/**
	 * Reload all the models and tasks informations.
	 */
	async function updateElements() {
		models = await getModels(idProject);
		modelsContent = [];
		for (var i = 0; i < models.length; i++) {
			let content = await getModelInformations(models[i].id);
			modelsContent.push(content);
		}
		modelsContent = modelsContent;
		model_id = models[0].id;
		model_name = models[0].name;
		await rootTreeView.updateTree();
	}

	/**
	 * Update the model for which we want to see the treeview.
	 *
	 * @param id	The id of the model (linked to the tree).
	 * @param name 	The name of the model (linked to the input).
	 */
	async function updateModelId(id: any, name: string) {
		model_id = id;
		model_name = name;
		await rootTreeView.updateTree();
	}

	/**
	 * Delete the current model and update the page without it.
	 */
	async function deleteModelInAPI(idModel: any) {
		await deleteModel(idModel);

		updateElements();
	}

	function comparePage() {
		if (browser) {
			goto('/compare/' + idProject);
		}
	}

	onMount(async function () {
		await updateElements();

		Split(['#split-0', '#split-1', '#split-2'], {
			sizes: [25, 50, 25],
			minSize: 0,
			snapOffset: 150,
			onDrag: function () {
				for (let i = 0; i < 3; i++) {
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
	<title>Models</title>
</svelte:head>

<div class="split">
	<div id="split-0">
		<button on:click={comparePage} type="button" class="col btn btn-outline-primary" style="margin-top: 20px;">Compare models</button>

		<h2 class="title">My models</h2>

		<div class="list-group list-group-flush" style="margin-bottom : 5px;">
			{#each modelsContent as model}
				<button type="button" class="list-group-item list-group-item-action model-content" on:click|stopPropagation={() => updateModelId(model.id, model.name)}>
					<div class="card-body d-flex justify-content-between">
						<span class="underline-on-hover">{model.name}</span>
						<div>
							<button on:click|stopPropagation={() => deleteModelInAPI(model.id)} type="button" class="btn btn-outline-danger btn-sm">Delete</button>
						</div>
					</div>
				</button>
			{/each}
		</div>

		<ModalCreationModel bind:model_id bind:model_name bind:rootTreeView bind:modify bind:idProject bind:models bind:modelsContent />
	</div>

	<div id="split-1">
		<HeaderButtonsModel bind:model_id bind:model_name bind:modify bind:modelsContent bind:models bind:idProject />

		<RootTreeView bind:this={rootTreeView} bind:modify bind:model_id />
	</div>

	<div id="split-2">
		<h2 class="title">Impact by resource</h2>
	</div>
</div>
