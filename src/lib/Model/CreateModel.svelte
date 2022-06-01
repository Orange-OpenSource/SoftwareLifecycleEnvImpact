<script>
import { post } from '$lib/api';

	import ModalComponent from '$lib/Modal.svelte';

	/* Bound vars */
	export let project;
	export let selectedModel;

	let modelName;

	async function createModel(){
		if(modelName != undefined && modelName != ''){
			const res = await post('models', {
				name: modelName,
				project_id: project.id,
			})

			if (res.status === 409) {
				alert('Model already exists');
			} else {
				modelName = ''
				project.models.push(res)
				selectedModel = res
				/*Redondant assignment to force Svelte to update components*/
				project.models = project.models
			}
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateModel" type="button" class="col-5 btn btn-light">Add model</button>

<ModalComponent details={'CreateModel'}>
	<span slot="title">Create new model</span>
	<form slot="body" on:submit|preventDefault={createModel}>
		<input id="createModelInput" placeholder="Model name" required bind:value={modelName}/>
		<button data-bs-dismiss="modal" type="submit" class="btn btn-primary">Create model</button>
	</form>
	
</ModalComponent>
