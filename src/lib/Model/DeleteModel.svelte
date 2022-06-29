<script>
	import { del } from '$lib/api';
	import Modal from '$lib/Modal.svelte';

	/*Bound var*/
	export let models;

	export let model;
	export let showModal;

	async function deleteModel(model) {
		const res = await del('models/'+model.id)
		
		if (res.status === 404) alert('No model project with this id');
		else if (res.status === 403) alert('Cannot delete the root model of a project');
		else{
			models = models.filter(m => m.id != model.id);
			showModal = false
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteModel(model)} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
