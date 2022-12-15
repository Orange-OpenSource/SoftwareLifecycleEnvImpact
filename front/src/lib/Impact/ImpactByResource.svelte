<script lang="ts">
	import type { EnvironmentalImpact, ResourcesImpact, Task } from '$lib/api/dataModel';
	import type { D3JSHierarchyNode, D3JStackedData } from '$lib/Dataviz/d3js';
	import StackedBarChart from '$lib/Dataviz/StackedBarChart.svelte';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import Treemap from '$lib/Dataviz/Treemap.svelte';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';
	import ImpactByIndicator from './ImpactByIndicator.svelte';

	export let impactByResource: ResourcesImpact;

	function convertResourcesImpactToHierarchy(): HierarchyNode<D3JSHierarchyNode> {
		let final: D3JSHierarchyNode = {
			name: 'root',
			children: []
		};

		for (const [resourceName, environmentalImpact] of Object.entries(impactByResource)) {
			final.children.push({
				name: resourceName,
				impact: environmentalImpact,
				// value: environmentalImpact.impacts['Climate change'].value,
				co2: environmentalImpact.impacts['Climate change'].value,
				children: []
			});
		}
		return hierarchy(final);
	}

	function convertResourcesImpactToStackedData(): D3JStackedData[] {
		let final: D3JStackedData[] = [];

		for (const [resourceName, environmentalImpact] of Object.entries(impactByResource)) {
			for (const [impactName, impactValue] of Object.entries(environmentalImpact.impacts)) {
				final.push({
					impactCategory: impactName,
					category: resourceName,
					value: impactValue.value
				});
			}
		}
		return final;
	}
</script>

<StackedBarChart chartData={convertResourcesImpactToStackedData()} />
<Sunburst hierarchy={convertResourcesImpactToHierarchy()} />
<!-- <Treemap hierarchy={convertResourcesImpactToHierarchy()} /> -->

{#if impactByResource != undefined}
	<ul>
		{#each Object.entries(impactByResource) as [key, value]}
			<li>
				{key}
				<ImpactByIndicator environmentalImpact={value} />
			</li>
		{/each}
	</ul>
{/if}
