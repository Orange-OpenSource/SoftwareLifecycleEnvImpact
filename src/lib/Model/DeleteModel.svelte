<script>
	import { del } from '$lib/api';
	import ModalComponent from '$lib/Modal.svelte';

	export let model;

	/**
	 * Delete the current model and update the page without it.
	 */
	async function deleteModel(model) {
		const res = await del('models/'+model.id)
		
		if (res.status === 404) alert('No model project with this id');
		else if (res.status === 403) alert('Cannot delete the root model of a project');
		else{
			/*models = models.filter(m => m.id != model.id);*/
		}
	}
</script>

<button on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalDeleteModel{model.id}" class="btn btn-light">Delete</button>

<ModalComponent details="DeleteModel{model.id}">
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteModel(model)} slot="btnsave" type="button" data-bs-dismiss="modal" class="btn btn-danger">Delete</button>
</ModalComponent>
