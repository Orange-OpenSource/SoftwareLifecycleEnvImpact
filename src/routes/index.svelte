<script lang="ts">
	import { onMount } from 'svelte';
	import { getProjects } from '../lib/controllers/RequestController';
	import { checkIfLogged } from '../lib/controllers/LoginController';

	checkIfLogged();

	let projects: any[] = [];

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
					<li class="list-group-item d-flex justify-content-between">
						<div class="card-body">
							<a id="redirect{project.id}" sveltekit:prefetch href="/view/{project.id}"
								>{project.name}</a
							>
						</div>
					</li>
				{/each}
			</ul>

			<button type="button" class="btn btn-light">New project</button>
		</div>
	</div>
</div>
