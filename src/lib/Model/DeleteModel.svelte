<script>
	import { del } from '$lib/api';
	import Modal from '$lib/Modal.svelte';

	/*Bound var*/
	export let models;

	export let model;

	let showModal;
	let error = ''

	async function deleteModel(model) {
		const res = await del('models/'+model.id)

		switch (res.status) {
			case undefined:
				models = models.filter(m => m.id != model.id);
				showModal = false
				break;
			case 404:
				error = 'No model project with this id'
				break;
			case 403:
				error = 'Cannot delete the root model of a project'
			default:
				error = res.status + ' error'
				break;
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>
	
	{#if error != ''}
		<p style="color: red">{error}</p>
	{/if}

	<button on:click|stopPropagation={() => deleteModel(model)} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
