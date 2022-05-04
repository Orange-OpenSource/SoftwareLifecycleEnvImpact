<script lang="ts">
	import { getModelInformations, getModels, createModel } from '$lib/controllers/RequestController';
	import Modal from './Modal.svelte';

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
</script>

<button
	data-bs-toggle="modal"
	data-bs-target="#modalCreateModel"
	type="button"
	class="btn btn-primary">Add model</button
>

<Modal details={'CreateModel'}>
	<span slot="title">Create new model</span>
	<input slot="body" id="createModelInput" placeholder="Model name" required />
	<button
		slot="btnsave"
		on:click={createNewModel}
		type="button"
		data-bs-dismiss="modal"
		class="btn btn-primary">Create model</button
	>
</Modal>
