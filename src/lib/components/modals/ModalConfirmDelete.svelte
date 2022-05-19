<script lang="ts">
	import { deleteModel, getModelInformations, getModels } from '$lib/controllers/RequestController';

	import ModalComponent from './ModalComponent.svelte';

	export let model: any;
	export let CURRENT_MODEL_NAME: string;
	export let CURRENT_MODEL_ID: any;
	export let idProject: any;
	export let models: any;
	export let modelsContent: any;
	export let rootTreeView: any;

	/**
	 * Delete the current model and update the page without it.
	 */
	async function deleteModelInAPI(idModel: any) {
		await deleteModel(idModel);

		models = await getModels(idProject);
		modelsContent = [];
		for (var i = 0; i < models.length; i++) {
			let content = await getModelInformations(models[i].id);
			modelsContent.push(content);
		}
		modelsContent = modelsContent;
		CURRENT_MODEL_ID = models[0].id;
		CURRENT_MODEL_NAME = models[0].name;
		await rootTreeView.updateTree();
	}
</script>

<ModalComponent details="DeleteModel{model.id}">
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteModelInAPI(model.id)} slot="btnsave" type="button" data-bs-dismiss="modal" class="btn btn-danger">Delete</button>
</ModalComponent>
