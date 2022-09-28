<script lang="ts">
	import type { AggregatedImpact, ResourcesImpact } from 'src/model/impacts';
	import ImpactByIndicator from './ImpactByIndicator.svelte';

	export let impactByResource: ResourcesImpact;
</script>

{#if impactByResource != undefined}
	<ul>
		{#each Object.entries(impactByResource) as [key, value]}
			<li>
				{key}
				<ImpactByIndicator impact={value} />
			</li>
		{/each}
	</ul>
{/if}
