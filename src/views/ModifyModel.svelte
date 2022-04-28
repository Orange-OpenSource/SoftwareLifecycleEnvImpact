<script>
    import RootTreeView from "../components/RootTreeView.svelte";
    import {createProject, updateModel, getModel} from "../controllers/RequestController";
    import { onMount } from "svelte";
    import { useNavigate } from "svelte-navigator";
    import HeaderButtonsModel from "../components/HeaderButtonsModel.svelte";

    const navigate = useNavigate();
    export let idModels;
    let isNew = false;
    let modify = true;
    let model_id, rootTreeView;

    async function saveProject() {
        let nameproject = document.getElementById("nameproject").value;
        if (isNew) {
            let newIdModel = await createProject(nameproject);
            navigate("../modify/" + newIdModel);
        } else {
            let newIdModel = await updateModel(idModels);
            navigate("../../modify/"+newIdModel);
        }
    }


    onMount(async function () {
        if (idModels != -1){
            model_id = idModels;
            await rootTreeView.updateTree();
        }
        else
            isNew = true;
	});
</script>

<div class="container">
    <div class="row h-100">
        <div class="col">
            <HeaderButtonsModel>
                <button type="button" class="col-2 btn btn-secondary" on:click={saveProject}>Save</button>
            </HeaderButtonsModel>
            
            <RootTreeView bind:this={rootTreeView} {modify} {model_id}></RootTreeView>
        </div>
    </div>
</div>