<script lang="ts">
	import { deleteModel, getModels } from '$lib/controllers/RequestController';
	import ModalComponent from '$lib/Modal.svelte';

	/* Bound var */
	export let model: any;

	/**
	 * Delete the current model and update the page without it.
	 */
	async function deleteModelInAPI(idModel: any) {
		await deleteModel(idModel);
	}
</script>

<button on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalDeleteModel{model.id}" class="btn btn-light">Delete</button>

<ModalComponent details="DeleteModel{model.id}">
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteModelInAPI(model.id)} slot="btnsave" type="button" data-bs-dismiss="modal" class="btn btn-danger">Delete</button>
</ModalComponent>
