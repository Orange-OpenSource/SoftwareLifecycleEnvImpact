<script lang="ts">
	import { getModelInformations, getModels, createModel } from '$lib/controllers/RequestController';
	import ModalComponent from './ModalComponent.svelte';

	export let idProject: string;
	export let models: string | any[] = [];
	export let modelsContent: any = [];
	export let modify: boolean;
	export let model_id: any;
	export let model_name: any;
	export let rootTreeView: any;

	async function createNewModel() {
		// @ts-ignore
		let name = document.getElementById('createModelInput').value;

		let res = await createModel(name, idProject);

		if (res.status === 409) {
			alert('Model already exists');
		} else {
			// @ts-ignore
			document.getElementById('createModelInput').value = '';

			models = await getModels(idProject);
			modelsContent = [];
			for (var i = 0; i < models.length; i++) {
				let content = await getModelInformations(models[i].id);
				modelsContent.push(content);
			}
			modelsContent = modelsContent;

			modify = true;
			model_id = res.id;
			model_name = res.name;
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
