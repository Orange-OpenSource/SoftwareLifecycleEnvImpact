<script>
	import { Link } from "svelte-navigator";
	import { onMount } from "svelte";
	import TreeViewModify from '../components/TreeViewModify.svelte';
	import RequestManager from '../controllers/RequestManager.svelte';
    import TreeView from '../components/TreeView.svelte';

	let requestManager;
	let children = [];
	let projects = [];

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

        <ul class="list-group list-group-flush">
			{#each projects as project}
				<li class="list-group-item"><Link to="view/{project.id}" style="color:black;">{project.name}</Link></li>
			{/each}
        </ul>

		<button type="button" on:click={requestManager.createProject}>
			New project
		</button>

      </div>
      <div class="col">
        <strong>Preview</strong>
        
        <div class="col scroll">
            <TreeView {children}></TreeView>
        </div>

      </div>
    </div>
</div>