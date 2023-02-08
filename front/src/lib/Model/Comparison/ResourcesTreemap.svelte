<script lang="ts">
	import { hierarchy, type HierarchyNode } from 'd3';
	import { impactValueTotal, type ResourcesImpact } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';
	import Treemap from '$lib/Dataviz/Treemap.svelte';

	export let resourcesImpact: ResourcesImpact;
	export let selectedImpactCategory: string;
	export let hierarchyPromise = convertToHierarchy();
	let svgElement: SVGSVGElement;

	async function convertToHierarchy(): Promise<HierarchyNode> {
		let final = {
			name: 'stocks',
			children: []
		};

		for (const [resourceName, resourceImpact] of Object.entries(resourcesImpact)) {
			const total = impactValueTotal(resourceImpact[selectedImpactCategory]).value;
			if (total) {
				final.children.push({
					name: resourceName,
					value: total
				});
			}
		}
		return hierarchy(final);
	}
</script>

<div class="col">
	{#await hierarchyPromise then hierarchy}
		<Treemap {hierarchy} />
	{:catch error}
		<Error message={error.message} />
	{/await}
</div>
