<script>
    import { del } from '$lib/api';
	import ModalComponent from '$lib/Modal.svelte';

	/* Bound var */
	export let projects;

	export let project;

	async function deleteProject(project) {
        const res = await del('projects/'+project.id)
		
        if (res.status === 404) alert('No project found with this id '+project.id);
		else{
			projects = projects.filter(p => p.id != project.id);
		}
	}
</script>

<button on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalDeleteProject{project.id}" class="btn btn-light">Delete</button>

<ModalComponent details="DeleteProject{project.id}">
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{project.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteProject(project)} slot="btnsave" type="button" data-bs-dismiss="modal" class="btn btn-danger">Delete</button>
</ModalComponent>