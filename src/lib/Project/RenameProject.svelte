<script>
	import { patch } from '$lib/api';
	import ModalComponent from '../Modal.svelte';

	/* Bound var */
	export let project;

	async function renameProject() {
		let newName = document.getElementById('createProjectInput' + project.id).value;

		const res = await patch('projects/' + project.id, [{
			op: 'replace',
			path: '/name',
			value: newName,
		}])

		if (res.status === 403) alert('Patch format is incorrect');
		else if (res.status === 404) alert('No project found with this id ' + project.id);
		else if (res.status === 409) {alert('Project already exists');}
		else{
			project.name = newName
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalRenameProject{project.id}" type="button" class="btn btn-outline-secondary btn-sm">Rename</button>

<ModalComponent details={'RenameProject' + project.id}>
	<span slot="title">Rename project :</span>
	<input slot="body" id="createProjectInput{project.id}" placeholder="Project new name" value={project.name} required />
	<button slot="btnsave" on:click={renameProject} type="button" data-bs-dismiss="modal" class="btn btn-primary">Rename project</button>
</ModalComponent>
