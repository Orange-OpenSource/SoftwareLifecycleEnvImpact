<script>
	import { post } from '$lib/api';
	import Modal from '$lib/Modal.svelte';

	/* Bound vars */
	export let project;
	export let selectedModel;

	let showModal = false;
	let modelName;
	let error = ''

	async function createModel(){
		if(modelName != undefined && modelName != ''){
			const res = await post('models', {
				name: modelName,
				project_id: project.id,
			})

			switch (res.status) {
                case undefined:
					modelName = ''
					project.models.push(res)
					selectedModel = res
					/*Redondant assignment to force Svelte to update components*/
					project.models = project.models
					showModal = false
                    break;
                case 409:
                    error = 'Model already exist'
                    break;
                default:
                    error = res.status + ' error'
                    break;
            }
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} type="button" class="col-5 btn btn-light">Add model</button>

<Modal bind:showModal>
	<span slot="title">Create new model</span>
	<form slot="body" on:submit|preventDefault={createModel}>
		<input id="createModelInput" placeholder="Model name" required bind:value={modelName}/>

		{#if error != ''}
			<p style="color: red">{error}</p>
		{/if}

		<button type="submit" class="btn btn-primary">Create model</button>
	</form>
	
</Modal>
