<script lang="ts">
	import type { ResourcesImpact } from '$lib/model/api/model/impacts';
	import ImpactByIndicator from './ImpactByIndicator.svelte';

	export let impactByResource: ResourcesImpact;
</script>

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
