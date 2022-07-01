<script>
	import { patch } from '$lib/api';
	import Modal from '../Modal.svelte';

	/* Bound var */
	export let project;

	let newName = project.name
	let showModal = false

	let error = ''

	async function renameProject() {
		const res = await patch('projects/' + project.id, [{
			op: 'replace',
			path: '/name',
			value: newName,
		}])

		switch (res.status) {
			case undefined:
				project.name = res.name
				showModal = false;
				break;
			case 403:
				error = 'Patch format is incorrect'
				break;
			case 404:
				error = 'No project found with this id ' + project.id
			case 409:
				error = 'Project already exists'
			default:
				error = res.status + ' error'
				break;
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} type="button" class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename project :</span>
	<form slot="body" on:submit|preventDefault={renameProject}>
		<input id="renameProjectInput{project.id}" placeholder="Project new name" bind:value={newName} required />
		
		{#if error != ''}
			<p style="color: red">{error}</p>
		{/if}
		<button type="submit" class="btn btn-primary">Rename project</button>
	</form>
</Modal>
