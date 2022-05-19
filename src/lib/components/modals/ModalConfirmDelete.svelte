<script lang="ts">
	import { deleteModel, getModels } from '$lib/controllers/RequestController';
	import ModalComponent from './ModalComponent.svelte';

	/* Bound var */
	export let CURRENT_MODEL_ID: any;
	export let CURRENT_MODEL_NAME: string;
	export let model: any;
	export let idProject: any;
	export let LIST_MODELS: any[];
	export let rootTreeView: any;

	/**
	 * Delete the current model and update the page without it.
	 */
	async function deleteModelInAPI(idModel: any) {
		await deleteModel(idModel);

		LIST_MODELS = await getModels(idProject);
		CURRENT_MODEL_ID = LIST_MODELS[0].id;
		CURRENT_MODEL_NAME = LIST_MODELS[0].name;
		await rootTreeView.updateTree();
	}
</script>

<ModalComponent details="DeleteModel{model.id}">
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteModelInAPI(model.id)} slot="btnsave" type="button" data-bs-dismiss="modal" class="btn btn-danger">Delete</button>
</ModalComponent>
