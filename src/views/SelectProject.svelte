<script>
	import { Link } from "svelte-navigator";
	import { onMount } from "svelte";
	import {loadPreview, getProjects} from '../controllers/RequestController';
    import TreeView from '../components/TreeView.svelte';

	let children = [];
	let projects = [];
	let modify = false;

	async function updatePreview(idProject) {
		children = await loadPreview(idProject);
	}

	onMount(async function () {
		projects = await getProjects();
		children = await loadPreview(1);
	});
</script>

<div class="container">
    <div class="row h-100">
      <div class="col-3 border-right h-100">
        <strong>My projects :</strong>

        <ul class="list-group list-group-flush ">
			{#each projects as project}
				<li class="list-group-item d-flex justify-content-between">
					<Link to="view/{project.id}" style="color:black;">{project.name}</Link>
					<button type="button" on:click={updatePreview(project.id)}>Preview</button>
				</li>
			{/each}
        </ul>

		<button type="button">
			<Link to="../modify" style="color:black; text-decoration: none; ">New project</Link>
		</button>

      </div>
      <div class="col">
        <strong>Preview</strong>
        
        <div class="col scroll">
            <TreeView {children} {modify}></TreeView>
        </div>

      </div>
    </div>
</div>