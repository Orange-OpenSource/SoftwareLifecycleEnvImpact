<script lang="ts">
	import { impactValueTotal, type ImpactSourceId, type ImpactSourceImpact, type Task, type TaskImpact } from '$lib/api/dataModel';
	import { constructLinks, type D3JSHierarchyNode, type D3JStackedData } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';
	import StackedBarChart from '$lib/Dataviz/StackedBarChart.svelte';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';

	export let impact: TaskImpact;

	/*Bound var*/
	export let selectedTask: Task;

	$: sourcesLinks = constructLinks(selectedTask, impact.sub_tasks, false, true);

	function convertResourcesImpactToHierarchy(): HierarchyNode<D3JSHierarchyNode> {
		let final: D3JSHierarchyNode = {
			name: 'root',
			children: getHierarchyChildrenNodes(impact.impact_sources)
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

		for (const [sourceName, sourceImpact] of Object.entries(impact.impact_sources)) {
			for (const [impactCategory, impactValue] of Object.entries(sourceImpact.total)) {
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

{#if Object.keys(impact.impact_sources).length}
	<div class="row">
		<h3>Resources:</h3>
	</div>

	<StackedBarChart chartData={convertResourcesImpactToStackedData()} />
	<Sunburst hierarchy={convertResourcesImpactToHierarchy()} />
	<Sankey links={sourcesLinks} />
	<!-- <Treemap hierarchy={convertResourcesImpactToHierarchy()} /> -->
{/if}
