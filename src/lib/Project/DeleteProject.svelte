<script>
    import { del } from '$lib/api';
	import Modal from '$lib/Modal.svelte';

	/* Bound var */
	export let projects;

	export let project;

	let showModal = false;

	async function deleteProject(project) {
        const res = await del('projects/'+project.id)
		
        if (res.status === 404) alert('No project found with this id '+project.id);
		else{
			projects = projects.filter(p => p.id != project.id);
			showModal = false
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true}  class="btn btn-light">Delete</button>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{project.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteProject(project)} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>