<script>
	import { Link, useNavigate } from "svelte-navigator";
	import { onMount } from "svelte";
	import TreeView from '../components/TreeView.svelte';

	const endpoint = 'https://626131b3327d3896e2767e8e.mockapi.io/projects';
	const navigate = useNavigate();

	let children = [];
	let projects = [];

	onMount(async function () {
		const response = await fetch(endpoint);
		projects = await response.json();

		const newresponse = await fetch(endpoint+"/1");
		let res = await newresponse.json();
		children = res.baseModel;
	});

	async function createProject () {
		const res = await fetch(endpoint, {
			method: 'POST'
		})

		const json = await res.json();

		navigate("visualisation/"+json.id);
	}

</script>

<div class="container">
    <div class="row h-100">
      <div class="col-3 border-right h-100">
        <strong>My projects :</strong>

        <ul class="list-group list-group-flush">
			{#each projects as project}
				<li class="list-group-item"><Link to="visualisation/{project.id}" style="color:black;">{project.name}</Link></li>
			{/each}
        </ul>

		<button type="button" on:click={createProject}>
			New project
		</button>

      </div>
      <div class="col">
        <strong>Preview</strong>
        
        <div class="col">
            <TreeView {children}></TreeView>
        </div>

      </div>
    </div>
</div>