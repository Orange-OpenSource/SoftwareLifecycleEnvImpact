<script lang="ts">
	import { getLastUpdate } from '$lib/utils';
	import type { Model } from '$lib/model/api/model/model';
	import type { Project } from '$lib/model/api/model/project';

	import CreateModel from './CreateModel.svelte';
	import DeleteModel from './DeleteModel.svelte';
	import DuplicateModel from './DuplicateModel.svelte';
	import RenameModel from './RenameModel.svelte';

	/*Bound vars*/
	export let selectedModel: Model;
	export let project: Project;
	export let selectedModels: Model[];
	export let compareModels: boolean;
</script>

<div class="col">
	<div class="row">
		<div class="list-group list-group-flush">
			{#if project != undefined && project.models != undefined}
				{#each project.models as model, i}
					<button type="button" class="list-group-item list-group-item-action" on:click|stopPropagation={() => (selectedModel = model)}>
						<div class="row">
							<div class="col-2">
								<input type="checkbox" class="form-check-input" value={model} bind:group={selectedModels} name={String(model.id)} on:click|stopPropagation={() => {}} />
							</div>
							<div class="col-7">
								<h5>
									{model.name}
								</h5>
								<small>{getLastUpdate(model)}</small>
							</div>
							<div class="col-3">
								<RenameModel bind:model />
								{#if i != 0}
									<DeleteModel {model} bind:models={project.models} />
								{/if}
								<DuplicateModel {model} bind:models={project.models} bind:selectedModel />
							</div>
						</div>
					</button>
				{/each}
			{:else}
				No model
			{/if}

			<div class="list-group-item">
				<div class="row justify-content-center">
					<div class="col-5">
						<button on:click|stopPropagation={() => (compareModels = true)} type="button" class="btn btn-light" disabled={selectedModels.length <= 1}> Compare </button>
					</div>
					<div class="col-5">
						<CreateModel bind:project bind:selectedModel />
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
