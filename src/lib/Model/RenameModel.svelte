<script>
	import { patch } from '$lib/api';
import Modal from '$lib/Modal.svelte';
	import ModalComponent from '$lib/Modal.svelte';

	/* Bound var */
	export let model;

	let newName = model.name

	async function renameModel() {
		const res = await patch('models/' + model.id, [{
			op: 'replace',
			path: '/name',
			value: newName,
		}])

		if (res.status === 403) alert('Patch format is incorrect');
		else if (res.status === 404) alert('No model found with this id' + model.id);
		else if (res.status === 409) {alert('Model already exists');}
		else{
			model.name = res.name
		}
	}
</script>

<button on:click|stopPropagation={() => {}} type="button" data-bs-toggle="modal" data-bs-target="#modalRenameModel{model.id}" class="btn btn-light">Rename</button>

<ModalComponent details={'RenameModel' + model.id}>
	<span slot="title">Rename model :</span>
	<form slot="body" on:submit|preventDefault={renameModel}>
		<input id="renameModelInput{model.id}" placeholder="Model new name" bind:value={newName} required />
		<button data-bs-dismiss="modal" type="submit" class="btn btn-primary">Rename model</button>
	</form>
	
</ModalComponent>
