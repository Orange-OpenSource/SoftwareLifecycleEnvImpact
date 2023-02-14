<script lang="ts">
	import { impactValueTotal, type EnvironmentalImpact, type ImpactSourceId, type ImpactSourceImpact, type Model } from '$lib/api/dataModel';
	import { getTaskImpact } from '$lib/api/task';
	import type { D3JGroupedData, D3JsDivergingData } from '$lib/Dataviz/d3js';
	import Error from '$lib/Error.svelte';
	import GroupedBarChart from '$lib/Dataviz/GroupedBarChart.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import DivergingBarChart from '$lib/Dataviz/DivergingBarChart.svelte';

	export let models: Model[];
	export let selectedImpactCategory: string;

	$: stackedData = getModelsImpactAsStackedData(selectedImpactCategory, models);
	$: divergingData = getModelsImpactAsDivergingData(selectedImpactCategory, models);
	let impactCatgories: EnvironmentalImpact;

	async function getModelsImpactAsStackedData(selectedImpactCategory: string, models: Model[]): Promise<D3JGroupedData[]> {
		let final: D3JGroupedData[] = [];
		for (let model in models) {
			let modelImpact = await getTaskImpact(models[model].root_task);

			if (impactCatgories == undefined) {
				// Little hack to retrieve the impact categories
				impactCatgories = modelImpact.total;
			}

			getResourcesStacked(selectedImpactCategory, models[model].name, final, modelImpact.impact_sources);
		}
		return final;
	}

	function getResourcesStacked(selectedImpactCategory: string, modelName: string, data: D3JGroupedData[], impacts: Record<ImpactSourceId, ImpactSourceImpact>) {
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
					getResourcesStacked(selectedImpactCategory, modelName, data, subImpact.sub_impacts);
				}
			}
		}
	}

	async function getModelsImpactAsDivergingData(selectedImpactCategory: string, models: Model[]): Promise<D3JsDivergingData[]> {
		let final: D3JsDivergingData[] = [];

		// First model
		let modelImpact = await getTaskImpact(models[0].root_task);
		getResourcesGrouped(true, selectedImpactCategory, models[0].name, final, modelImpact.impact_sources);
		// Little hack to retrieve the impact categories
		if (impactCatgories == undefined) {
			impactCatgories = modelImpact.total;
		}

		// Second model
		modelImpact = await getTaskImpact(models[1].root_task);
		getResourcesGrouped(false, selectedImpactCategory, models[1].name, final, modelImpact.impact_sources);

		return final;
	}

	function getResourcesGrouped(isFirstModel: boolean, selectedImpactCategory: string, modelName: string, data: D3JsDivergingData[], impacts: Record<ImpactSourceId, ImpactSourceImpact>) {
		if (impacts) {
			for (const [sourceName, sourceImpact] of Object.entries(impacts)) {
				const total = impactValueTotal(sourceImpact.own_impact[selectedImpactCategory]).value;
				if (total) {
					if (isFirstModel) {
						data.push({
							first: total,
							second: 0,
							name: sourceName
						});
					} else {
						let a = data.find((x) => x.name === sourceName);
						if (a) a.second = total;
					}
				}
				for (const [_, subImpact] of Object.entries(sourceImpact.sub_impacts)) {
					// Recursive call for childrens
					getResourcesGrouped(isFirstModel, selectedImpactCategory, modelName, data, subImpact.sub_impacts);
				}
			}
		}
	}
</script>

{#await divergingData}
	<Spinner />
{:then impact}
	<div class="d-flex">
		<select class="form-select" bind:value={selectedImpactCategory} required>
			{#each Object.entries(impactCatgories) as [key, _]}
				<option value={key} class="form-check-input">{key}</option>
			{/each}
		</select>
	</div>
	<!-- <GroupedBarChart chartData={impact} /> -->
	<DivergingBarChart chartData={impact} />
{:catch error}
	<Error message={error.message} />
{/await}
