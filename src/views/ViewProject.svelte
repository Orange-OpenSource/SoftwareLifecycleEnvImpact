<script>
    import { onMount } from "svelte";
    import { getModels, getModelInformations } from '../controllers/RequestController';
    import RootTreeView from '../components/RootTreeView.svelte';
    import HeaderButtonsModel from "../components/HeaderButtonsModel.svelte";
    
    export let idProject;
    let models = [];
    export let modelsContent;

    let modify = false;
    export let model_id;
    let rootTreeView;

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
        modelsContent = [];
        for (var i = 0; i < models.length; i++) {
  			let content = await getModelInformations(models[i].id);
			modelsContent.push(content);
		}
        modelsContent = modelsContent;
        model_id = models[0].id;
        await rootTreeView.updateTree();
	});
</script>

<div class="container">
    <div class="row">
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