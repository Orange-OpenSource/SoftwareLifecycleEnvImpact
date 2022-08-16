<script lang="ts">
	import { del } from '$lib/api/api';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from 'src/model/model';

	/* TODO update models when one is deleted */
	/*Bound var*/
	//export let models: Model[];

	export let model: Model;

	let showModal: boolean;
	let error = '';

	async function deleteModel(model: Model) {
		const res = await del('models/' + model.id);

		switch (res.status) {
			case undefined:
				//models = models.filter(m => m.id != model.id);
				showModal = false;
				break;
			case 404:
				error = 'No model project with this id';
				break;
			case 403:
				error = 'Cannot delete the root model of a project';
			default:
				error = res.status + ' error';
				break;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{model.name}</strong> ?</span>

	{#if error != ''}
		<p style="color: red">{error}</p>
	{/if}

	<button on:click|stopPropagation={() => deleteModel(model)} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
