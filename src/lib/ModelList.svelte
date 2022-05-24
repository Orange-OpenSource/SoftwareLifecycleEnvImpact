<script>
	export let models;

    /*Bound var*/
    export let selectedModel;

    function updateModelSelected(model) { /*TODO maybe useless ? */
		selectedModel = model
	}
    
</script>

<div class="list-group list-group-flush" style="margin-bottom : 5px;">
    {#each models as model, i}
        
        
        <button type="button" class="list-group-item list-group-item-action model-content" on:click|stopPropagation={() => updateModelSelected(model)} style="padding-bottom: 20px">
        {model.name}    
        </button>
        




        <!--
        <button type="button" class="list-group-item list-group-item-action model-content" on:click|stopPropagation={() => updateModelId(model.id, model.name)} style="padding-bottom: 20px">
            <div class="card-body d-flex justify-content-between" style="padding-bottom:0px">
                <div>
                    <input on:click={updateComparaison} type="checkbox" class="modelsInput" value={model.id} name={model.id} />
                    <span class="underline-on-hover">
                        {model.name}
                        {#if i == 0}
                            <strong>(default)</strong>
                        {/if}
                    </span>
                </div>
                <div class="d-flex justify-content-center">
                    <div on:click|stopPropagation={() => {}} type="button" data-bs-toggle="modal" data-bs-target="#modalRenameModel{model.id}" class="icon-grey">
                        <TiPencil />
                    </div>

                    {#if i != 0}
                        <div on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalDeleteModel{model.id}" class="icon-red">
                            <TiDelete />
                        </div>
                    {/if}
                </div>
            </div>
            <span class="d-flex align-items-start" style="color:grey; font-size : 12px">Last modified : {getLastUpdate(model)}</span>
        </button>
-->
        <!--
        <svelte:component this={ModalRenameModel} bind:models bind:idProject bind:model bind:CURRENT_MODEL_NAME />

        <ModalConfirmDelete bind:CURRENT_MODEL_ID bind:CURRENT_MODEL_NAME bind:LIST_MODELS bind:idProject bind:model bind:rootTreeView />
-->
        {/each}
</div>