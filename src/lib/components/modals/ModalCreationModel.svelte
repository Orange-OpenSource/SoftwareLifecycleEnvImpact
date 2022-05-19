<script lang="ts">
	import { getModels, createModel } from '$lib/controllers/RequestController';
	import ModalComponent from './ModalComponent.svelte';

	/* Bound var */
	export let idProject: string;
	export let LIST_MODELS: any[] = [];
	export let modify: boolean;
	export let CURRENT_MODEL_ID: any;
	export let CURRENT_MODEL_NAME: any;
	export let rootTreeView: any;

	/**
	 * Create a new model and set the treeview to the new model.
	 */
	async function createNewModel() {
		// @ts-ignore
		let name = document.getElementById('createModelInput').value;

		let res = await createModel(name, idProject);

		if (res.status === 409) {
			alert('Model already exists');
		} else {
			// @ts-ignore
			document.getElementById('createModelInput').value = '';

			LIST_MODELS = await getModels(idProject);
			modify = true;
			CURRENT_MODEL_ID = res.id;
			CURRENT_MODEL_NAME = res.name;
			rootTreeView.updateTree();
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateModel" type="button" class="col-5 btn btn-light">Add model</button>

<ModalComponent details={'CreateModel'}>
	<span slot="title">Create new model</span>
	<div slot="body">
		<input id="createModelInput" placeholder="Model name" required />
	</div>
	<button slot="btnsave" data-bs-dismiss="modal" on:click={createNewModel} type="button" class="btn btn-primary">Create model</button>
</ModalComponent>
