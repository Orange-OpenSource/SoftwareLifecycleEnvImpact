<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { getModels, getModelInformations, deleteModel } from '$lib/controllers/RequestController';
	import RootTreeView from '$lib/components/RootTreeView.svelte';
	import HeaderButtonsModel from '$lib/components/HeaderButtonsModel.svelte';
	import { checkIfLogged } from '$lib/controllers/LoginController';
	import ModalCreationModel from '$lib/components/modals/ModalCreationModel.svelte';

	checkIfLogged();

	let idProject = $page.params.id;
	let models: string | any[] = [];
	let modelsContent: any = [];
	let modify = false;
	let model_id: any;
	let rootTreeView: any;
	let model_name: string;

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

	async function updateModelId(id: any, name: string) {
		model_id = id;
		model_name = name;
		await rootTreeView.updateTree();
	}

	async function handleMessage(event: { detail: { text: any } }) {
		models = await getModels(idProject);
		modelsContent = [];
		for (var i = 0; i < models.length; i++) {
			let content = await getModelInformations(models[i].id);
			modelsContent.push(content);
		}
		modelsContent = modelsContent;
	}

	async function deleteModelInAPI() {
		await deleteModel(model_id);

		updateElements();
	}

	onMount(async function () {
		await updateElements();
	});

	function isSelected(id: any) {
		return id === model_id;
	}
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

<div class="container">
	<div class="row" style="margin-top: 5px; border-bottom: solid 1px #ddd;">
		<div class="col">
			<select class="form-select" aria-label="Default select example">
				{#each modelsContent as model, i}
					<option
						selected={isSelected(model.id)}
						on:click={() => updateModelId(model.id, model.name)}>{model.name}</option
					>
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

			<ModalCreationModel
				bind:model_id
				bind:model_name
				bind:rootTreeView
				bind:modify
				bind:idProject
				bind:models
				bind:modelsContent
			/>
		</div>
	</div>

	<div class="row">
		<div class="col border-right">
			<HeaderButtonsModel on:message={handleMessage} bind:model_id bind:model_name bind:modify />

			<RootTreeView bind:this={rootTreeView} {modify} bind:model_id />
		</div>

		<div class="col-3">
			<h2 class="title">Impact by resource</h2>
		</div>
	</div>
</div>
