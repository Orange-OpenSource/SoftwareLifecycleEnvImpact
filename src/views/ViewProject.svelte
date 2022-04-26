<script>
	import { onMount } from "svelte";
    import RequestManager from '../controllers/RequestManager.svelte';
    import TreeView from '../components/TreeView.svelte';
    import { Link } from "svelte-navigator";
    
	export let idProject;
    let requestManager;
	let children = []
    let models = []
    let modify = false;

	async function updatePreviewModel(idModel) {
		children = await requestManager.getModel(idModel);
	}

	onMount(async function () {
        children = await requestManager.loadPreview(idProject);
        models = await requestManager.getModels(idProject);
	});
</script>

<RequestManager bind:this={requestManager} />

<div class="container">

    <div class="row h-100">

        <div class="col col-3 border-right h-100">
            <strong>My models :</strong>

            <ul class="list-group list-group-flush">
                {#each models as model}
                    <li class="list-group-item d-flex justify-content-between">
                        <Link to="../../modify/{model}" style="color:black;">{model}</Link>
                        <button type="button" on:click={updatePreviewModel(model)}>Preview</button>
                    </li>
                {/each}
            </ul>

            <button type="button">
                New model
            </button>
        </div>

        <div class="col">

            <div class="row" style="padding-top : 20px;">
                <span class="col-4">
                    <input type="email" class="form-control" id="nameproject" placeholder="Name project">
                </span>
                <button type="button" class="col-3 btn btn-light" style="margin-right: 20px;">Compare</button>
                <button type="button" class="col-3 btn btn-light">Project</button>
            </div>

            <strong>Preview</strong>
            
            <div class="col scroll">
                <TreeView {children} {modify}></TreeView>
            </div>

        </div>

        <div class="col-3 border-left h-100">
          Impact by resource
        </div>
    </div>
</div>