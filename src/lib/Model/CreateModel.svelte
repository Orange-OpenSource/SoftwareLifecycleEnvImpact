<script>
import { post } from '$lib/api';

	import ModalComponent from '$lib/Modal.svelte';

	/* Bound var */
	export let project;

	/**
	 * Create a new model and set the treeview to the new model.
	 */
	async function createNewModel() {
		let nameModel = document.getElementById('createModelInput').value;

		const res = await post('models', {
			name: nameModel,
			project_id: project.id,
		})

		if (res.status === 409) {
			alert('Model already exists');
		} else {
			document.getElementById('createModelInput').value = '';
			project.models.push(res)
			/*Redondant assignment to force Svelte to update components*/
			project.models = project.models
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateModel" type="button" class="col-5 btn btn-light">Add model</button>

<ModalComponent details={'CreateModel'}>
	<span slot="title">Create new model</span>
	<div slot="body">
		<input id="createModelInput" placeholder="Model name" required />
	</div>
	<button slot="btnsave" data-bs-dismiss="modal" on:click={createNewModel} type="button" class="btn btn-primary">Create model</button>
</ModalComponent>
