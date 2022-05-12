<script lang="ts">
	import { getModelInformations, getModels, updateModel } from '$lib/controllers/RequestController';
	import ModalComponent from './ModalComponent.svelte';
	import { Modal } from 'bootstrap';

	export let model: any;
	export let idProject: any;
	export let models: any;
	export let modelsContent: any;
	export let model_name: string;
	let error: string = '';

	/**
	 * Update the name of the model.
	 */
	async function renameModel() {
		// @ts-ignore
		let newName = document.getElementById('renameModelInput' + model.id).value;
		let oldname = model.name;

		let res = await updateModel(model.id, newName);

		if (res.status === 409) {
			error = 'Model already exists';
		} else {
			error = '';
			let myModal = document.getElementById('modalRenameModel' + model.id)!;
			let modal = Modal.getInstance(myModal);
			modal!.hide();
			document.querySelector('div.modal-backdrop.fade.show')!.remove();

			models = await getModels(idProject);
			modelsContent = [];
			for (var i = 0; i < models.length; i++) {
				let content = await getModelInformations(models[i].id);
				modelsContent.push(content);
			}
			modelsContent = modelsContent;

			if (oldname == model_name) model_name = newName;
		}
	}
</script>

<ModalComponent details={'RenameModel' + model.id}>
	<span slot="title">Rename model :</span>
	<div slot="body">
		<input id="renameModelInput{model.id}" placeholder="Model new name" value={model.name} required />
		{#if error}
			<div id="error_message" class="text-danger">
				<small>{error}</small>
			</div>
		{/if}
	</div>
	<button slot="btnsave" on:click={renameModel} type="button" class="btn btn-primary">Rename project</button>
</ModalComponent>
