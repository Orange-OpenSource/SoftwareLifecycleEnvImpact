<script lang="ts">
	import { getModelInformations, getModels, createModel } from '$lib/controllers/RequestController';
	import { Modal } from 'bootstrap';
	import ModalComponent from './ModalComponent.svelte';

	export let idProject: string;
	export let models: string | any[] = [];
	export let modelsContent: any = [];
	export let modify: boolean;
	export let model_id: any;
	export let model_name: any;
	export let rootTreeView: any;
	let error: string = '';

	async function createNewModel() {
		// @ts-ignore
		let name = document.getElementById('createModelInput').value;

		let res = await createModel(name, idProject);

		if (res.status === 409) {
			error = 'Model already exists';
		} else {
			error = '';
			let myModal = document.getElementById('modalCreateModel')!;
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
		{#if error}
			<div id="error_message" class="text-danger">
				<small>{error}</small>
			</div>
		{/if}
	</div>
	<button slot="btnsave" on:click={createNewModel} type="button" class="btn btn-primary">Create model</button>
</ModalComponent>
