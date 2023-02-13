<script lang="ts">
	import { impactValueTotal, type EnvironmentalImpact, type ImpactSourceId, type ImpactSourceImpact, type Model } from '$lib/api/dataModel';
	import { getTaskImpact } from '$lib/api/task';
	import type { D3JGroupedData } from '$lib/Dataviz/d3js';
	import Error from '$lib/Error.svelte';
	import GroupedBarChart from '$lib/Dataviz/GroupedBarChart.svelte';
	import Spinner from '$lib/Spinner.svelte';

	export let models: Model[];
	export let selectedImpactCategory: string;

	$: subtasksLinks = getModelsImpactAsStackedData(selectedImpactCategory, models);
	let impactCatgories: EnvironmentalImpact;

	async function getModelsImpactAsStackedData(selectedImpactCategory: string, models: Model[]): Promise<D3JGroupedData[]> {
		let final: D3JGroupedData[] = [];
		for (let model in models) {
			let modelImpact = await getTaskImpact(models[model].root_task);

			if (impactCatgories == undefined) {
				// Little hack to retrieve the impact categories
				impactCatgories = modelImpact.total;
			}

			getResourcesNodes(selectedImpactCategory, models[model].name, final, modelImpact.impact_sources);
		}
		return final;
	}

	function getResourcesNodes(selectedImpactCategory: string, modelName: string, data: D3JGroupedData[], impacts: Record<ImpactSourceId, ImpactSourceImpact>) {
		if (impacts) {
			for (const [sourceName, sourceImpact] of Object.entries(impacts)) {
				const total = impactValueTotal(sourceImpact.own_impact[selectedImpactCategory]).value;
				if (total) {
					data.push({
						resourceName: sourceName,
						modelName: modelName,
						value: total
					});
				}
				for (const [_, subImpact] of Object.entries(sourceImpact.sub_impacts)) {
					// Recursive call for childrens
					getResourcesNodes(selectedImpactCategory, modelName, data, subImpact.sub_impacts);
				}
			}
		}
	}
</script>

{#await subtasksLinks}
	<Spinner />
{:then impact}
	<div class="d-flex">
		<select class="form-select" bind:value={selectedImpactCategory} required>
			{#each Object.entries(impactCatgories) as [key, _]}
				<option value={key} class="form-check-input">{key}</option>
			{/each}
		</select>
	</div>
	<GroupedBarChart chartData={impact} />
{:catch error}
	<Error message={error.message} />
{/await}
