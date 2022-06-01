<script>
	import { getLastUpdate } from '$lib/utils';

	import CreateModel from './CreateModel.svelte';
	import DeleteModel from './DeleteModel.svelte';
	import RenameModel from './RenameModel.svelte';

	/*Bound vars*/
	export let selectedModel;
	export let project;

	function updateModelSelected(model) {
		/*TODO maybe useless ? */
		selectedModel = model;
	}
</script>

{#if project != undefined}
	<div>
		<div class="list-group list-group-flush">
			{#each project.models as model, i}
				<button type="button" class="list-group-item list-group-item-action link" on:click|stopPropagation={() => updateModelSelected(model)}>
					<div class="row">
						<div class="col align-self-center">
							<input type="checkbox" class="form-check-input" value={model.id} name={model.id} />
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
											<DeleteModel bind:models={project.models} {model} />
										{/if}
								</div>
							</div>
						</div>
					</div>
				</button>
			{/each}
		</div>
		<CreateModel bind:project />
	</div>
{/if}

