<script>
    import TreeViewModify from "../components/TreeViewModify.svelte";
    import RequestManager from "../controllers/RequestManager.svelte";
    import { onMount } from "svelte";

    export let idModels;
    let requestManager;

    let children = [];

    onMount(async function () {
        children = await requestManager.getModel(idModels);
	});
</script>

<RequestManager bind:this={requestManager} />

<div class="container">

    <div class="row h-100">

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
                <TreeViewModify {children}></TreeViewModify>
            </div>

        </div>
    </div>
</div>