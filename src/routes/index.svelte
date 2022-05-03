<script lang="ts">
	import { onMount } from 'svelte';
	import { deleteProject, getProjects } from '../lib/controllers/RequestController';
	import { checkIfLogged } from '../lib/controllers/LoginController';
	import ModalCreationProjectComponent from '$lib/components/ModalCreationProjectComponent.svelte';

	checkIfLogged();

	let projects: any[] = [];

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
								<a id="redirect{project.id}" sveltekit:prefetch href="/view/{project.id}"
									>{project.name}</a
								>
								<button
									on:click={() => deleteProjectInAPI(project.id)}
									type="button"
									class="btn btn-secondary btn-sm">Delete</button
								>
							</div>
						</div>
					</li>
				{/each}
			</ul>

			<button
				data-bs-toggle="modal"
				data-bs-target="#modalCreate"
				type="button"
				class="btn btn-light">New project</button
			>

			<ModalCreationProjectComponent />
		</div>
	</div>
</div>
