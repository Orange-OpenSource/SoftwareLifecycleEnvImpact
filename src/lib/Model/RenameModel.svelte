<script>
	import { patch } from '$lib/api';
	import ModalComponent from '$lib/Modal.svelte';

	/* Bound var */
	export let model;

	/**
	 * Update the name of the model.
	 */
	async function renameModel() {
		let newName = document.getElementById('renameModelInput' + model.id).value;

		const res = patch('models/' + model.id, [{
			op: 'replace',
			path: '/name',
			value: newName,
		}])

		if (res.status === 403) alert('Patch format is incorrect');
		else if (res.status === 404) alert('No model found with this id' + model.id);
		else if (res.status === 409) {alert('Model already exists');}
	}
</script>

<button on:click|stopPropagation={() => {}} type="button" data-bs-toggle="modal" data-bs-target="#modalRenameModel{model.id}" class="btn btn-light">Rename</button>

<ModalComponent details={'RenameModel' + model.id}>
	<span slot="title">Rename model :</span>
	<div slot="body">
		<input id="renameModelInput{model.id}" placeholder="Model new name" value={model.name} required />
	</div>
	<button slot="btnsave" data-bs-dismiss="modal" on:click={renameModel} type="button" class="btn btn-primary">Rename project</button>
</ModalComponent>
