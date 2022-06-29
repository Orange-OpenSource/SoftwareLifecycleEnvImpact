<script>
	import { patch } from '$lib/api';
	import Modal from '../Modal.svelte';

	/* Bound var */
	export let project;

	let newName = project.name
	let showModal = false

	async function renameProject() {
		const res = await patch('projects/' + project.id, [{
			op: 'replace',
			path: '/name',
			value: newName,
		}])

		if (res.status === 403) alert('Patch format is incorrect');
		else if (res.status === 404) alert('No project found with this id ' + project.id);
		else if (res.status === 409) {alert('Project already exists');}
		else{
			project.name = res.name
			showModal = false;
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} type="button" class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename project :</span>
	<form slot="body" on:submit|preventDefault={renameProject}>
		<input id="renameProjectInput{project.id}" placeholder="Project new name" bind:value={newName} required />
		<button type="submit" class="btn btn-primary">Rename project</button>
	</form>
</Modal>
