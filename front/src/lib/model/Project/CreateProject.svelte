<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { createProjectRequest, importProjectRequest } from '$lib/model/api/project';
	import Error from '$lib/Error.svelte';
	import Modal from '$lib/Modal.svelte';

	let projectName: string;
	let showModal = false;
	let error = '';

	let files: FileList;

	$: showModal, (error = ''); //Clean error message when closing modal

	async function createNewProject() {
		error = '';
		try {
			let res;
			if (files && files[0]) {
				console.log('here')
				var reader = new FileReader();
				reader.readAsText(files[0], 'UTF-8');
				reader.onload = async function (event) {
					if (reader.result != null) {
						res = await importProjectRequest(reader.result.toString());
					}
				};
			} else {
				res = await createProjectRequest(projectName);
			}
			showModal = false;
			if (browser && res != undefined) goto('/project/' + res.id);
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="btn btn-light">New project</button>

<Modal bind:showModal>
	<span slot="title">Create new project</span>
	<form slot="body" on:submit|preventDefault={createNewProject}>
		<input id="createProjectInput" placeholder="Project name" required bind:value={projectName} />
		{#if error}
			<Error message={error} slot="error" />
		{/if}
		<input type="file" accept=".json" bind:files />

		<button type="submit" class="btn btn-primary">Create project</button>
	</form>
</Modal>
