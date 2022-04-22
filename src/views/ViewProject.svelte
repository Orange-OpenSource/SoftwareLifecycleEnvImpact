<script>
	import TreeView from '../components/TreeView.svelte';
	import { onMount } from "svelte";
    import RequestManager from '../controllers/RequestManager.svelte';
    
	export let idProject;
    let requestManager;
	let children = []

	onMount(async function () {
        children = await requestManager.loadPreview(idProject);
	});
</script>

<RequestManager bind:this={requestManager} />

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