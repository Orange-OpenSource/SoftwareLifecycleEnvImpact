<script lang="ts">
	import { onMount } from 'svelte';
	import { deleteProject, getProjects } from '$lib/controllers/RequestController';
	import { checkIfLogged } from '$lib/controllers/LoginController';
	import ModalCreationProject from '$lib/components/modals/ModalCreationProject.svelte';
	import ModalRenameProject from '$lib/components/modals/ModalRenameProject.svelte';
	import { getCreationDate } from '$lib/utils/dates';

	checkIfLogged();

	let projects: any[] = [];

	/**
	 * Delete the project in API and update page without it.
	 *
	 * @param project_id
	 */
	async function deleteProjectInAPI(project_id: any) {
		await deleteProject(project_id);
		projects = await getProjects();
	}

	onMount(async function () {
		projects = await getProjects();
	});
</script>

<svelte:head>
	<title>Projects</title>
</svelte:head>

<div class="container">
	<div class="row">
		<div class="col">
			<h2 class="title">My projects</h2>

			<ul class="list-group list-group-flush" style="margin-bottom : 5px;">
				{#each projects as project}
					<li class="list-group-item">
						<div class="card-body d-flex justify-content-center">
							<div class="d-flex justify-content-between" style="width: 40%;">
								<a id="redirect{project.id}" sveltekit:prefetch href="/project/{project.id}">{project.name}</a>
								<div>
									<ModalRenameProject bind:projects {project} />
									<button on:click={() => deleteProjectInAPI(project.id)} type="button" class="btn btn-outline-danger btn-sm">Delete</button>
								</div>
							</div>
						</div>
						<span class="d-flex justify-content-center" style="color:grey; font-size : 12px">Created at : {getCreationDate(project.created_at)}</span>
					</li>
				{/each}
			</ul>

			<ModalCreationProject />
		</div>
	</div>
</div>
