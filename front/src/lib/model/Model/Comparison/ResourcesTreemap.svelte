<script lang="ts">
	import { hierarchy, type HierarchyNode } from 'd3';
	import type { ResourcesImpact } from '$lib/model/api/model/impacts';
	import Treemap from '$lib/model/Treemap.svelte';
	import Error from '$lib/Error.svelte';

	export let resourcesImpact: ResourcesImpact;
	export let hierarchyPromise = convertToHierarchy();
	let svgElement: SVGSVGElement;

	async function convertToHierarchy(): Promise<HierarchyNode> {
		let final = {
			name: 'stocks',
			children: []
		};

		for (const [key, value] of Object.entries(resourcesImpact)) {
			final.children.push({
				name: key,
				value: value['Climate change'].value
			});
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
