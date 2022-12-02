<script lang="ts">
	import { hierarchy, type HierarchyNode } from 'd3';
	import Treemap from '$lib/Treemap.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import type { ResourcesImpact, Model, TaskImpact, SubtasksImpact } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';
	import { getTaskImpact } from '$lib/api/task';
	import Sunburst from '$lib/Sunburst.svelte';

	export let models: Model[];
	let modelsImpactPromise = retrieveModelsImpacts();

	$: models, (modelsImpactPromise = retrieveModelsImpacts());

	async function retrieveModelsImpacts(): Promise<Map<Model, TaskImpact>> {
		let returnDict = new Map<Model, TaskImpact>();
		for (const model of models) {
			let modelImpact = await getTaskImpact(model.root_task);
			console.log(modelImpact);
			returnDict.set(model, modelImpact);
		}
		return returnDict;
	}

	function convertResourcesImpactToHierarchy(resourceImpact: ResourcesImpact): HierarchyNode {
		let final = {
			name: 'root',
			children: []
		};

		for (const [resourceName, environmentalImpact] of Object.entries(resourceImpact)) {
			final.children.push({
				name: resourceName,
				value: environmentalImpact.impacts['Climate change'].value
			});
		}
		return hierarchy(final);
	}
</script>

<div class="row">
	{#await modelsImpactPromise}
		<Spinner />
	{:then modelsImpact}
		<h5>Resource</h5>
		{#each [...modelsImpact] as [model, modelImpact]}
			<div class="col">
				<div class="row">
					<h1>{model.name}</h1>
				</div>
				<div class="row">
					<h3>Tasks:</h3>
				</div>
				<div class="row">
					<h3>Resources:</h3>
				</div>
				{#await convertResourcesImpactToHierarchy(modelImpact.resources) then hierarchy}
					<div class="row">
						<Sunburst {hierarchy} />
					</div>
					<div class="row">
						<Treemap {hierarchy} />
					</div>
				{:catch error}
					<Error message={error.message} />
				{/await}
			</div>
		{/each}
	{:catch error}
		<Error message={error.message} />
	{/await}
</div>
