<script>
	import TreeView from '../components/TreeView.svelte';
	import { onMount } from "svelte";
    
	export let idProject;

	console.log(idProject);

	let children = []

	const endpoint = 'https://626131b3327d3896e2767e8e.mockapi.io/projects/';
	let project = [];

	onMount(async function () {
		const response = await fetch(endpoint + idProject);
		project = await response.json();
		children = project.baseModel;
		console.log(project);
	});
</script>

<div class="container">

    <div class="row h-100">

      <div class="col">

        <div class="row" style="padding-top : 20px;">
            <div style="max-width : 200px;">
                <input type="email" class="form-control" id="nameproject" placeholder="Name project">
            </div>
            <button type="button" class="btn btn-light" style="max-width : 200px; margin-right: 20px;">Compare</button>
            <button type="button" class="btn btn-light" style="max-width : 200px;">Project</button>
        </div>

        <strong>Preview</strong>
        
        <div class="col">
            <TreeView {children}></TreeView>
        </div>

      </div>

      <div class="col-3 border-left h-100">
          Impact by resource
      </div>
    </div>
</div>