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
</script>

<div>
	{#if project != undefined && project.models != undefined}
		<div class="list-group list-group-flush">
			{#each project.models as model, i}
				<button type="button" class="list-group-item list-group-item-action" on:click|stopPropagation={() => (selectedModel = model)}>
					<div class="row">
						<div class="col-2">
							<input type="checkbox" class="form-check-input" value={model} bind:group={selectedModels} name={String(model.id)} on:click|stopPropagation={() => console.log('hello')} />
						</div>
						<div class="col-7">
							<h5>
								{model.name}
								{#if i == 0}
									(default)
								{/if}
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
		</div>
	{:else}
		No model
	{/if}
	<CreateModel bind:project bind:selectedModel />
</div>
