<script lang="ts">
	import { getModelInformations, getModels, updateModel } from '$lib/controllers/RequestController';
	import ModalComponent from './ModalComponent.svelte';

	export let model: any;
	export let idProject: any;
	export let models: any;
	export let modelsContent: any;
	export let CURRENT_MODEL_NAME: string;

	/**
	 * Update the name of the model.
	 */
	async function renameModel() {
		// @ts-ignore
		let newName = document.getElementById('renameModelInput' + model.id).value;
		let oldname = model.name;

		let res = await updateModel(model.id, newName);

		if (res.status === 409) {
			alert('Model already exists');
		} else {
			models = await getModels(idProject);
			modelsContent = [];
			for (var i = 0; i < models.length; i++) {
				let content = await getModelInformations(models[i].id);
				modelsContent.push(content);
			}
			modelsContent = modelsContent;

			if (oldname == CURRENT_MODEL_NAME) CURRENT_MODEL_NAME = newName;
		}
	}
</script>

<ModalComponent details={'RenameModel' + model.id}>
	<span slot="title">Rename model :</span>
	<div slot="body">
		<input id="renameModelInput{model.id}" placeholder="Model new name" value={model.name} required />
	</div>
	<button slot="btnsave" data-bs-dismiss="modal" on:click={renameModel} type="button" class="btn btn-primary">Rename project</button>
</ModalComponent>
