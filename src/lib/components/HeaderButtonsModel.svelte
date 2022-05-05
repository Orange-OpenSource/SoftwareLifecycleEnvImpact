<script lang="ts">
	import { getModelInformations, getModels, updateModel } from '$lib/controllers/RequestController';

	export let idProject: any;
	export let model_id: any;
	export let model_name: string;
	export let modify: boolean;
	export let models: string | any[];
	export let modelsContent: any;

	function enableModifications() {
		modify = true;
	}

	/**
	 * Update the name of the model.
	 */
	async function renameModel() {
		modify = false;
		// @ts-ignore
		let newName = document.getElementById('nameproject').value;
		if (newName !== model_name) {
			await updateModel(model_id, newName);
			model_name = newName;
			models = await getModels(idProject);
			modelsContent = [];
			for (var i = 0; i < models.length; i++) {
				let content = await getModelInformations(models[i].id);
				modelsContent.push(content);
			}
			modelsContent = modelsContent;
		}
	}
</script>

<div class="row" style="padding : 20px 0px 0px 10px; margin-bottom: 20px;">
	<span class="col-4">
		<input class="form-control" id="nameproject" placeholder="Name project" value={model_name} readonly={!modify} />
	</span>
	{#if modify}
		<button on:click={renameModel} type="button" class="col-4 btn btn-secondary">Preview mode</button>
	{:else}
		<button id="modifybtn" on:click={enableModifications} type="button" class="col-4 btn btn-primary" style="margin-right: 10px;">Editing mode</button>
	{/if}
</div>
