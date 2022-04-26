<script>
    import { onMount } from "svelte";
    import { getModels } from '../controllers/RequestController';
    import RootTreeView from '../components/RootTreeView.svelte';
    import { Link } from "svelte-navigator";
    import HeaderButtonsModel from "../components/HeaderButtonsModel.svelte";
    
    export let idProject;
    let models = []
    let modify = false;
    let model_id, rootTreeView;

    async function updatePreviewModel(newIdModel) {
        model_id = newIdModel;
        await rootTreeView.updateTree();
    }

    function enableModifications() {
        modify = true;
    }

    function saveProject() {
        // todo : gestion sauvegarde projet
        modify = false;
    }

    onMount(async function () {
        models = await getModels(idProject);
        model_id = models[0];
        await rootTreeView.updateTree();
	});
</script>

<div class="container">
    <div class="row">
        <div class="col col-3 border-right">
            <h2 class="title">My models :</h2>

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

        <div class="col border-right">
            {#if modify}
                <HeaderButtonsModel>
                    <button on:click={saveProject} type="button" class="col-2 btn btn-secondary">Save</button>
                </HeaderButtonsModel>
            {:else}
                <HeaderButtonsModel>
                    <button on:click={enableModifications} type="button" class="col-2 btn btn-primary" style="margin-right: 10px;">Modify</button>
                </HeaderButtonsModel>
            {/if}
            
            <RootTreeView bind:this={rootTreeView} {modify} {model_id}></RootTreeView>
        </div>

        <div class="col-3">
          <h2 class="title">Impact by resource</h2>
        </div>
    </div>
</div>