<script lang="ts">
	import { impactValueTotal, type ImpactSourceId, type ImpactSourceImpact, type Task, type TaskImpact } from '$lib/api/dataModel';
	import { constructLinks, type D3JSHierarchyNode, type D3JStackedData } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';
	import StackedBarChart from '$lib/Dataviz/StackedBarChart.svelte';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';

	export let impact: TaskImpact;
	export let selectedImpactCategory: string;

	/*Bound var*/
	export let selectedTask: Task;

	$: sourcesLinks = constructLinks(selectedImpactCategory, selectedTask, impact, false, true);

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
			const total = impact.total_impact[selectedImpactCategory];
			const manufacture = total.manufacture && total.manufacture.value ? total.manufacture.value : 0;
			const use = total.use && total.use.value ? total.use.value : 0;
			if (total) {
				returnValue.push({
					name: sourceName,
					impact: impact.total_impact,
					manufacture: manufacture,
					use: use,
					children: getHierarchyChildrenNodes(impact.sub_impacts)
				});
			}
		}
		return returnValue;
	}

	function convertResourcesImpactToStackedData(): D3JStackedData[] {
		let final: D3JStackedData[] = [];
		getResourcesNodes(final, impact.impact_sources);
		return final;
	}

	function getResourcesNodes(data: D3JStackedData[], impacts: Record<ImpactSourceId, ImpactSourceImpact>) {
		if (impacts && Object.keys(impact).length > 0) {
			for (const [sourceName, sourceImpact] of Object.entries(impacts)) {
				for (const [impactCategory, impactValue] of Object.entries(sourceImpact.own_impact)) {
					const total = impactValueTotal(impactValue).value;

					if (total) {
						// Search if sourceName already pushed
						let existingData = data.find((x) => x.category === sourceName && x.impactCategory === impactCategory);

						if (existingData) {
							// If already push, add to the right value
							existingData.value += total;
						} else {
							// If not, create the associated entry
							data.push({
								impactCategory: impactCategory,
								category: sourceName,
								value: total
							});
						}
					}
				}
				//Recursive call
				getResourcesNodes(data, sourceImpact.sub_impacts);
			}
		}
	}
</script>

{#if Object.keys(impact.impact_sources).length}
	<div class="row">
		<h3>Resources:</h3>
	</div>

	<StackedBarChart chartData={convertResourcesImpactToStackedData()} />
	<!-- <StackedBarChart chartData={TESTconvertResourcesImpactToStackedData()} /> -->
	<!-- <Sunburst hierarchy={convertResourcesImpactToHierarchy()} /> -->
	<Sankey links={sourcesLinks} />
	<!-- <Treemap hierarchy={convertResourcesImpactToHierarchy()} /> -->
{/if}
