<script lang="ts">
	import { getLastUpdate } from '$lib/utils';
	import type { Model } from 'src/model/model';
	import type { Project } from 'src/model/project';

	import CreateModel from './CreateModel.svelte';
	import DeleteModel from './DeleteModel.svelte';
	import RenameModel from './RenameModel.svelte';

	/*Bound vars*/
	export let selectedModel: Model;
	export let project: Project;
</script>

<div>
	<div class="list-group list-group-flush">
		{#if project != undefined && project.models != undefined}
			{#each project.models as model, i}
				<button type="button" class="list-group-item list-group-item-action link" on:click|stopPropagation={() => (selectedModel = model)}>
					<div class="row">
						<div class="col align-self-center">
							<input type="checkbox" class="form-check-input" value={model.id} name={String(model.id)} />
						</div>
						<div class="col-10">
							<div class="row">
								<div class="col {selectedModel === model ? 'text-primary' : ''}">
									<h5 class="mb-1">
										{model.name}
										{#if i == 0}
											<strong>(default)</strong>
										{/if}
									</h5>
									<small>{getLastUpdate(model)}</small>
								</div>
								<div class="col-9">
									<RenameModel bind:model />
									{#if i != 0}
										<DeleteModel {model} />
									{/if}
								</div>
							</div>
						</div>
					</div>
				</button>
			{/each}
		{:else}
			No model
		{/if}

	</div>
	<CreateModel bind:project={project} bind:selectedModel={selectedModel} />
</div>