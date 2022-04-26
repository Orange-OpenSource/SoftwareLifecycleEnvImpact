<script>
	import { Link } from "svelte-navigator";
	import { onMount } from "svelte";
	import {getOriginalModelId, getProjects} from '../controllers/RequestController';
    import RootTreeView from '../components/RootTreeView.svelte';

	let projects = [];
	let modify = false;
	let model_id, rootTreeView;

	async function updatePreview(idProject) {
		model_id = await getOriginalModelId(idProject);
		
        rootTreeView.updateTree();
	}

	onMount(async function () {
		projects = await getProjects();
		model_id = await getOriginalModelId(1);
		rootTreeView.updateTree();
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
			<RootTreeView bind:this={rootTreeView} {modify} {model_id}></RootTreeView>
        </div>

      </div>
    </div>
</div>