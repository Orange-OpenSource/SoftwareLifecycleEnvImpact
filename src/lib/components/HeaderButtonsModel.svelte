<script lang="ts">
	import { updateModel } from '$lib/controllers/RequestController';
	import { createEventDispatcher } from 'svelte';

	export let model_id: any;
	export let model_name: string;
	export let modify: boolean;

	const dispatch = createEventDispatcher();

	function enableModifications() {
		modify = true;
	}

	async function saveProject() {
		modify = false;
		// @ts-ignore
		let newName = document.getElementById('nameproject').value;
		if (newName !== model_name) {
			await updateModel(model_id, newName);
			model_name = newName;
			dispatch('message', {
				text: 'updateModelName'
			});
		}
	}
</script>

<div class="row" style="padding-top : 20px; margin-bottom: 20px;">
	<span class="col-3">
		<input
			type="email"
			class="form-control"
			id="nameproject"
			placeholder="Name project"
			value={model_name}
			readonly={!modify}
		/>
	</span>
	<button type="button" class="col-3 btn btn-light" style="margin-right: 10px;">Compare</button>
	{#if modify}
		<button on:click={saveProject} type="button" class="col-3 btn btn-secondary">Save</button>
	{:else}
		<button
			id="modifybtn"
			on:click={enableModifications}
			type="button"
			class="col-3 btn btn-primary"
			style="margin-right: 10px;">Modify</button
		>
	{/if}
</div>
