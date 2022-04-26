<script>
    import TreeView from "../components/TreeView.svelte";
    import RequestManager from "../controllers/RequestManager.svelte";
    import { onMount } from "svelte";
    import { useNavigate } from "svelte-navigator";

    const navigate = useNavigate();
    export let idModels;
    let requestManager;
    let isNew = false;
    let modify = true;

    let children = [];

    async function saveProject() {
        if (isNew) {
            let newIdModel = await requestManager.createProject();
            navigate("../modify/" + newIdModel);
        } else {
            let newIdModel = await requestManager.updateModel(idModels);
            navigate("../../modify/"+newIdModel);
        }
    }

    onMount(async function () {
        if (idModels != -1)
            children = await requestManager.getModel(idModels);
        else
            isNew = true;
	});
</script>

<RequestManager bind:this={requestManager} />

<div class="container">

    <div class="row h-100">

        <div class="col">

            <div class="row" style="padding-top : 20px;">
                <span class="col-3">
                    <input type="email" class="form-control" id="nameproject" placeholder="Name project">
                </span>
                <button type="button" class="col-2 btn btn-light" style="margin-right: 20px;">Compare</button>
                <button type="button" class="col-2 btn btn-light" style="margin-right: 20px;">Projects</button>
                <button type="button" class="col-2 btn btn-secondary" on:click={saveProject}>Save</button>
            </div>

            <strong>Preview</strong>
            
            <div class="col scroll">
                <TreeView {children} {modify}></TreeView>
            </div>

        </div>
    </div>
</div>