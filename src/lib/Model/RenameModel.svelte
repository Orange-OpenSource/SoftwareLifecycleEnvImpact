<script>
	import { updateModel } from '$lib/controllers/RequestController';
	import ModalComponent from '$lib/Modal.svelte';

	/* Bound var */
	export let model;

	/**
	 * Update the name of the model.
	 */
	async function renameModel() {
		let newName = document.getElementById('renameModelInput' + model.id).value;
		let oldname = model.name;

		let res = await updateModel(model.id, newName);

		if (res.status === 409) {
			alert('Model already exists');
		}
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
