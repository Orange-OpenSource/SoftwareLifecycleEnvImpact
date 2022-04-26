<script>
    import RootTreeView from "../components/RootTreeView.svelte";
    import {createProject, updateModel, getModel} from "../controllers/RequestController";
    import { onMount } from "svelte";
    import { useNavigate } from "svelte-navigator";

    const navigate = useNavigate();
    export let idModels;
    let isNew = false;
    let modify = true;
    let model_id, rootTreeView;

    async function saveProject() {
        if (isNew) {
            let newIdModel = await createProject();
            navigate("../modify/" + newIdModel);
        } else {
            let newIdModel = await updateModel(idModels);
            navigate("../../modify/"+newIdModel);
        }
    }

    onMount(async function () {
        if (idModels != -1){
            model_id = idModels;
            rootTreeView.updateTree();
        }
        else
            isNew = true;
	});
</script>

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
                <RootTreeView bind:this={rootTreeView} {modify} {model_id}></RootTreeView>
            </div>

        </div>
    </div>
</div>