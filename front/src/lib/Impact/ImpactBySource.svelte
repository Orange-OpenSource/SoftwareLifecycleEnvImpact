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
			const total = impact.own_impact[selectedImpactCategory];
			const manufacture = total.manufacture && total.manufacture.value ? total.manufacture.value : 0;
			const use = total.use && total.use.value ? total.use.value : 0;
			if (total) {
				returnValue.push({
					name: sourceName,
					impact: impact.own_impact,
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
		if (impacts) {
			for (const [sourceName, sourceImpact] of Object.entries(impacts)) {
				for (const [impactCategory, impactValue] of Object.entries(sourceImpact.own_impact)) {
					const total = impactValueTotal(impactValue).value;
					if (total) {
						data.push({
							impactCategory: impactCategory,
							category: sourceName,
							value: total
						});
					}
				}
				for (const [_, subImpact] of Object.entries(sourceImpact.sub_impacts)) {
					// Recursive call for childrens
					getResourcesNodes(data, subImpact.sub_impacts);
				}
			}
		}
	}

	function TESTconvertResourcesImpactToStackedData(): D3JStackedData[] {
		let final: D3JStackedData[] = [];

		for (const [sourceName, sourceImpact] of Object.entries(impact.impact_sources)) {
			for (const [impactCategory, impactValue] of Object.entries(sourceImpact.own_impact)) {
				if (impactValue.manufacture && impactValue.manufacture.value) {
					final.push({
						impactCategory: 'Manufacture',
						category: sourceName,
						value: impactValue.manufacture.value
					});
				}
				if (impactValue.use && impactValue.use.value) {
					final.push({
						impactCategory: 'Use',
						category: sourceName,
						value: impactValue.use.value
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
	<!-- <StackedBarChart chartData={TESTconvertResourcesImpactToStackedData()} /> -->
	<Sunburst hierarchy={convertResourcesImpactToHierarchy()} />
	<Sankey links={sourcesLinks} />
	<!-- <Treemap hierarchy={convertResourcesImpactToHierarchy()} /> -->
{/if}
