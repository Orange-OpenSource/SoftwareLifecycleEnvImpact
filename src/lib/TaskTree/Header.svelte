<script lang="ts">
	import { getModels, updateModel } from '$lib/controllers/RequestController';

	export let selectedModel: any;

	/* Bound var */
	export let modify: boolean;

	async function changeState() {
		// @ts-ignore
		let state = document.getElementById('editmodeSwitch').checked;

		if (state) enableModifications();
		else await renameModel();
	}

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
		if (newName !== selectedModel.name) {
			await updateModel(selectedModel, newName);
		}
	}

</script>

{#if selectedModel == undefined}
	<div>No model selected</div>
{:else}
<div class="row" style="padding : 20px 0px 0px 10px; margin-bottom: 20px;">
	<span class="col-4">
		<input class="form-control" id="nameproject" placeholder="Name project" value={selectedModel.name} readonly={!modify} />
	</span>

	<div class="col-4 form-check form-switch" style="margin:5px 0px 0px 10px;">
		<input on:click={changeState} class="form-check-input" type="checkbox" id="editmodeSwitch" checked={modify} />
		<label class="form-check-label" style="width:100px;" for="editmodeSwitch">Editing mode</label>
	</div>
</div>
{/if}



