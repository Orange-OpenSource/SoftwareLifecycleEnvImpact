<script lang="ts">
	import { impactValueTotal, type ImpactSourceId, type ImpactSourceImpact, type Task } from '$lib/api/dataModel';
	import type { D3JSHierarchyNode, D3JStackedData } from '$lib/Dataviz/d3js';
	import StackedBarChart from '$lib/Dataviz/StackedBarChart.svelte';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';

	export let impactBySource: Record<ImpactSourceId, ImpactSourceImpact>;

	function convertResourcesImpactToHierarchy(): HierarchyNode<D3JSHierarchyNode> {
		let final: D3JSHierarchyNode = {
			name: 'root',
			children: getHierarchyChildrenNodes(impactBySource)
		};

		return hierarchy(final);
	}

	function getHierarchyChildrenNodes(subImpacts: Record<ImpactSourceId, ImpactSourceImpact>): D3JSHierarchyNode[] {
		let returnValue: D3JSHierarchyNode[] = [];
		for (const [sourceName, impact] of Object.entries(subImpacts)) {
			const total = impactValueTotal(impact.total['Climate change']).value;
			if (total) {
				returnValue.push({
					name: sourceName,
					impact: impact.total,
					// value: environmentalImpact['Climate change'].value,
					co2: total,
					children: getHierarchyChildrenNodes(impact.sub_impacts)
				});
			}
		}
		return returnValue;
	}

	function convertResourcesImpactToStackedData(): D3JStackedData[] {
		let final: D3JStackedData[] = [];

		for (const [sourceName, impact] of Object.entries(impactBySource)) {
			for (const [impactCategory, impactValue] of Object.entries(impact.total)) {
				const total = impactValueTotal(impactValue).value;
				if (total) {
					final.push({
						impactCategory: impactCategory,
						category: sourceName,
						value: total
					});
				}
			}
		}
		return final;
	}
</script>

{#if Object.keys(impactBySource).length}
	<div class="row">
		<h3>Resources:</h3>
	</div>

	<StackedBarChart chartData={convertResourcesImpactToStackedData()} />
	<Sunburst hierarchy={convertResourcesImpactToHierarchy()} />
	<!-- <Treemap hierarchy={convertResourcesImpactToHierarchy()} /> -->
{/if}
