<!-- BSD 3-Clause License

Copyright (c) 2017, Orange
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. -->
<script lang="ts">
	import { impactValueTotal, type ImpactSourceId, type ImpactSourceImpact, type Activity, type ActivityImpact } from '$lib/api/dataModel';
	import { constructLinks, type D3JSHierarchyNode, type D3JStackedData } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';
	import StackedBarChart from '$lib/Dataviz/StackedBarChart.svelte';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';

	export let impact: ActivityImpact;
	export let selectedImpactCategory: string;

	/*Bound var*/
	export let selectedActivity: Activity;

	$: sourcesLinks = constructLinks(selectedImpactCategory, selectedActivity, impact, false, true);

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
