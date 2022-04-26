<script>
	import { Link } from "svelte-navigator";
	import { onMount } from "svelte";
	import RequestManager from '../controllers/RequestManager.svelte';
    import TreeView from '../components/TreeView.svelte';

	let requestManager;
	let children = [];
	let projects = [];
	let modify = false;

	async function updatePreview(idProject) {
		children = await requestManager.loadPreview(idProject);
	}

	onMount(async function () {
		projects = await requestManager.getProjects();
		children = await requestManager.loadPreview(1);
	});
</script>

<RequestManager bind:this={requestManager} />

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