<script lang="ts">
	import type { ResourcesImpact } from '$lib/api/dataModel';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import Treemap from '$lib/Dataviz/Treemap.svelte';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';
	import ImpactByIndicator from './ImpactByIndicator.svelte';

	export let impactByResource: ResourcesImpact;

	function convertResourcesImpactToHierarchy(): HierarchyNode {
		let final = {
			name: 'root',
			children: []
		};

		for (const [resourceName, environmentalImpact] of Object.entries(impactByResource)) {
			final.children.push({
				name: resourceName,
				value: environmentalImpact.impacts['Climate change'].value
			});
		}
		return hierarchy(final);
	}
</script>

<Sunburst hierarchy={convertResourcesImpactToHierarchy()}/>
<Treemap hierarchy={convertResourcesImpactToHierarchy()}/>

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
