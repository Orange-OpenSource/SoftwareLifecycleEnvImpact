<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { createProjectRequest, importProjectRequest } from '$lib/api/project';
	import Error from '$lib/Error.svelte';
	import Modal from '$lib/Modal.svelte';

	let projectName: string;
	let showModal = false;
	let error = '';

	let files: FileList;

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		projectName = '';
	}

	async function createNewProject() {
		error = '';
		try {
			let res;
			if (files && files[0]) {
				var reader = new FileReader();
				reader.readAsText(files[0], 'UTF-8');
				reader.onload = async function (event) {
					try {
						if (reader.result != null) {
							res = await importProjectRequest(reader.result.toString());
							if (browser && res != undefined) goto('/project/' + res.id);
						}
					} catch (e: any) {
						error = e.message;
					}
				};
			} else {
				res = await createProjectRequest(projectName);
				if (browser && res != undefined) goto('/project/' + res.id);
			}
		} catch (e: any) {
			error = e.message;
		}
	}

	function updateName() {
		if (files != undefined && files[0] != undefined && files[0].name != undefined) projectName = files[0].name.replace('.json', '');
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} type="button" class="btn btn-light">New project</button>

<Modal bind:showModal>
	<span slot="title">Create new project</span>
	<form slot="body" on:submit|preventDefault={createNewProject}>
		<div class="row g-3">
			<div class="col-12">
				<label for="createModelInput">Name</label>
				<input id="createModelInput" class="form-control" placeholder="Project name" required bind:value={projectName} />
			</div>
			<div class="col-12">
				<label for="loadFile">Load from file</label>
				<input id="loadFile" type="file" class="form-control" accept=".json" bind:files on:change={(e) => updateName()} />
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-primary">Create project</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
