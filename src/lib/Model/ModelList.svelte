<script>
	import { getLastUpdate } from '$lib/utils/dates';
	import CreateModel from './CreateModel.svelte';
	import DeleteModel from './DeleteModel.svelte';
	import RenameModel from './RenameModel.svelte';

	export let models;
    export let projectId;

	/*Bound var*/
	export let selectedModel;

	function updateModelSelected(model) {
		/*TODO maybe useless ? */
		selectedModel = model;
	}

	function updateComparaison() {
		/*TODO comparison function/route*/
	}
</script>

<div>
	<div class="list-group list-group-flush" style="margin-bottom : 5px;">
		{#each models as model, i}
			<button type="button" class="list-group-item list-group-item-action" on:click|stopPropagation={() => updateModelSelected(model)} style="padding-bottom: 20px">
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
                        <!--
						<RenameModel bind:model />
                        -->
						{#if i != 0}
							<DeleteModel bind:model />
						{/if}
					</div>
				</div>
				<span class="d-flex align-items-start" style="color:grey; font-size : 12px">Last modified : {getLastUpdate(model)}</span>
			</button>
		{/each}
	</div>

    <CreateModel {projectId}/>
</div>
