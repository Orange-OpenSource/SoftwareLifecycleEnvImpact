<script>
	import { Link } from "svelte-navigator";
	import { onMount } from "svelte";
	import { getProjects } from '../controllers/RequestController';

	let projects = [];

	onMount(async function () {
		projects = await getProjects();
	});
</script>

<div class="container">
    <div class="row">
		<div class="col">
			<h2 class="title">My projects</h2>

			<ul class="list-group list-group-flush ">
				{#each projects as project}
					<li class="list-group-item d-flex justify-content-between">
						<div class="card-body">
						<Link to="view/{project.id}" style="color:black; font-size: large;">{project.name}</Link>
						</div>
					</li>
				{/each}
			</ul>

			<button type="button" class="btn btn-light">
				<Link to="../modify" style="color:black; text-decoration: none; ">New project</Link>
			</button>
      	</div>
    </div>
</div>