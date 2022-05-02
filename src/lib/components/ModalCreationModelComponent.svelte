<script lang="ts">
	import { getModelInformations, getModels, createModel } from '../controllers/RequestController';

	export let idProject: string;
	export let models: string | any[] = [];
	export let modelsContent: any = [];

	async function createNewModel() {
		// @ts-ignore
		let name = document.getElementById('createModelInput').value;

		await createModel(name, idProject);

		models = await getModels(idProject);
		modelsContent = [];
		for (var i = 0; i < models.length; i++) {
			let content = await getModelInformations(models[i].id);
			modelsContent.push(content);
		}
		modelsContent = modelsContent;
	}
</script>

<div
	class="modal fade"
	id="modalCreateModel"
	tabindex="-1"
	aria-labelledby="modalLabelCreateModel"
	aria-hidden="true"
>
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="modalLabelCreateModel">Create new model :</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>
			<div class="modal-body">
				<input id="createModelInput" placeholder="Model name" required />
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
				<button
					on:click={createNewModel}
					type="button"
					data-bs-dismiss="modal"
					class="btn btn-primary">Create model</button
				>
			</div>
		</div>
	</div>
</div>
