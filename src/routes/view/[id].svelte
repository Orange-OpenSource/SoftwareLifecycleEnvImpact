<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { getModels, getModelInformations, deleteModel } from '$lib/controllers/RequestController';
	import RootTreeView from '$lib/components/RootTreeView.svelte';
	import HeaderButtonsModel from '$lib/components/HeaderButtonsModel.svelte';
	import { checkIfLogged } from '$lib/controllers/LoginController';
	import ModalCreationModel from '$lib/components/modals/ModalCreationModel.svelte';
	import Split from 'split.js'

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
	async function deleteModelInAPI(idModel : any) {
		await deleteModel(idModel);

		updateElements();
	}

	onMount(async function () {
		await updateElements();

		Split(['#split-0', '#split-1', '#split-2'], {
			sizes : [25, 50, 25],
			minSize: 0,
			snapOffset: 150,
			onDrag : function() {
				for (let i = 0; i < 3; i++) {
					let element = document.getElementById('split-' + i);
					if (element!.offsetWidth === 0){
						element!.style.visibility = "hidden";
					} else {
						element!.style.visibility = "visible";
					}
				}
			}
		})
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

	<div class="split">
		<div id="split-0">
			<h2 class="title">My models</h2>

			<ul class="list-group list-group-flush" style="margin-bottom : 5px;">
				{#each modelsContent as model}
					<li class="list-group-item">
						<div class="card-body d-flex justify-content-between">
								<span on:click={() => updateModelId(model.id, model.name)} class="underline-on-hover" style="cursor:pointer;">{model.name}</span>
								<div>
									<button on:click={() => deleteModelInAPI(model.id)} type="button" class="btn btn-outline-danger btn-sm">Delete</button>
								</div>
						</div>
					</li>
				{/each}
			</ul>

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

<style>

</style>