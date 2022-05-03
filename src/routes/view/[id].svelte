<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import {
		getModels,
		getModelInformations,
		deleteModel
	} from '../../lib/controllers/RequestController';
	import RootTreeView from '../../lib/components/RootTreeView.svelte';
	import HeaderButtonsModel from '../../lib/components/HeaderButtonsModel.svelte';
	import { checkIfLogged } from '../../lib/controllers/LoginController';
	import ModalCreationModelComponent from '$lib/components/ModalCreationModelComponent.svelte';

	checkIfLogged();

	let idProject = $page.params.id;
	let models: string | any[] = [];
	let modelsContent: any = [];
	let modify = false;
	let model_id: any;
	let rootTreeView: any;
	let model_name: string;

	function enableModifications() {
		modify = true;
	}

	function saveProject() {
		// todo : gestion sauvegarde projet
		modify = false;
	}

	async function updateModelId(id: any, name: string) {
		model_id = id;
		model_name = name;
		await rootTreeView.updateTree();
	}

	async function deleteModelInAPI() {
		await deleteModel(model_id);

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

	onMount(async function () {
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
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

<div class="container">
	<div class="row" style="margin-top: 5px; border-bottom: solid 1px #ddd;">
		<div class="col">
			<select class="form-select" aria-label="Default select example">
				{#each modelsContent as model, i}
					<option on:click={() => updateModelId(model.id, model.name)}>{model.name}</option>
				{/each}
			</select>
		</div>
		<div class="col d-flex justify-content-end">
			<button
				on:click={deleteModelInAPI}
				type="button"
				class="btn btn-secondary"
				style="margin-right:5px;">Delete current model</button
			>
			<button
				data-bs-toggle="modal"
				data-bs-target="#modalCreateModel"
				type="button"
				class="btn btn-primary">Add model</button
			>

			<ModalCreationModelComponent {idProject} bind:models bind:modelsContent />
		</div>
	</div>

	<div class="row">
		<div class="col border-right">
			{#if modify}
				<HeaderButtonsModel bind:model_name>
					<button on:click={saveProject} type="button" class="col-3 btn btn-secondary">Save</button>
				</HeaderButtonsModel>
			{:else}
				<HeaderButtonsModel bind:model_name>
					<button
						id="modifybtn"
						on:click={enableModifications}
						type="button"
						class="col-3 btn btn-primary"
						style="margin-right: 10px;">Modify</button
					>
				</HeaderButtonsModel>
			{/if}

			<RootTreeView bind:this={rootTreeView} {modify} bind:model_id />
		</div>

		<div class="col-3">
			<h2 class="title">Impact by resource</h2>
		</div>
	</div>
</div>
