<script lang="ts">
	import Spinner from '$lib/Spinner.svelte';
	import type { ResourcesImpact, Model } from '$lib/api/dataModel';
	import ResourcesTreemap from './ResourcesTreemap.svelte';
	import Error from '$lib/Error.svelte';
	import { getTaskImpact } from '$lib/api/task';

	export let models: Model[];
	let modelsImpactPromise = retrieveModelsImpacts();

	$: models, (modelsImpactPromise = retrieveModelsImpacts());

	async function retrieveModelsImpacts(): Promise<Map<Model, ResourcesImpact>> {
		let returnDict = new Map<Model, ResourcesImpact>();
		for (const model of models) {
			let modelImpact = await getTaskImpact(model.root_task);
			returnDict.set(model, modelImpact.resources);
		}
		return returnDict;
	}
</script>

<div class="row">
	{#await modelsImpactPromise}
		<Spinner />
	{:then modelsImpact}
		<h5>Resource</h5>
		{#each [...modelsImpact] as [key, value]}
			<div class="col">
				<div class="row">
					{key.name}
				</div>
				<div class="row">
					<ResourcesTreemap resourcesImpact={value} />
				</div>
			</div>
		{/each}
	{:catch error}
		<Error message={error.message} />
	{/await}
</div>
