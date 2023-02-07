<script lang="ts">
	import { duplicateModelRequest } from '$lib/api/model';
	import Modal from '$lib/Modal.svelte';
	import type { Model } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';
	import Icon from '@iconify/svelte';

	/*Bound var*/
	export let models: Model[];
	export let selectedModel: Model;

	export let model: Model;

	let showModal = false;
	let error = 'd';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}
	async function duplicateModel() {
		error = '';
		try {
			const res = await duplicateModelRequest(model);
			models.push(res);
			selectedModel = res;
			/*Redundant assignement to force svelte to update components*/
			models = models;
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button class="btn" on:click|stopPropagation={() => (showModal = true)}>
	<Icon icon="ion:duplicate-outline" width="25" height="25" alt="Duplicate" loading="lazy" />
</button>

<Modal bind:showModal
	>a
	<span slot="title">Confirm duplicate</span>

	<form slot="body" on:submit|preventDefault={duplicateModel}>
		<div class="row g-3">
			<div class="col-12">
				Are you sure you want to duplicate <strong>{model.name}</strong> ?
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn">Duplicate</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
