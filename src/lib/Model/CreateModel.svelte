<script>
import { post } from '$lib/api';

	import Modal from '$lib/Modal.svelte';

	/* Bound vars */
	export let project;
	export let selectedModel;

	let showModal = false;
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
				showModal = false
			}
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} type="button" class="col-5 btn btn-light">Add model</button>

<Modal bind:showModal>
	<span slot="title">Create new model</span>
	<form slot="body" on:submit|preventDefault={createModel}>
		<input id="createModelInput" placeholder="Model name" required bind:value={modelName}/>
		<button type="submit" class="btn btn-primary">Create model</button>
	</form>
	
</Modal>
