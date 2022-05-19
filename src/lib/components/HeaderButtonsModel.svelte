<script lang="ts">
	import { getModelInformations, getModels, updateModel } from '$lib/controllers/RequestController';

	export let idProject: any;
	export let CURRENT_MODEL_ID: any;
	export let CURRENT_MODEL_NAME: string;
	export let modify: boolean;
	export let models: string | any[];
	export let modelsContent: any;

	async function changeState() {
		// @ts-ignore
		let state = document.getElementById('editmodeSwitch').checked;

		if (state) {
			enableModifications();
		} else {
			await renameModel();
		}
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
		if (newName !== CURRENT_MODEL_NAME) {
			await updateModel(CURRENT_MODEL_ID, newName);
			CURRENT_MODEL_NAME = newName;
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
		<input class="form-control" id="nameproject" placeholder="Name project" value={CURRENT_MODEL_NAME} readonly={!modify} />
	</span>

	<div class="col-4 form-check form-switch" style="margin:5px 0px 0px 10px;">
		<input on:click={changeState} class="form-check-input" type="checkbox" id="editmodeSwitch" checked={modify} />
		<label class="form-check-label" style="width:100px;" for="editmodeSwitch">Editing mode</label>
	</div>
</div>
