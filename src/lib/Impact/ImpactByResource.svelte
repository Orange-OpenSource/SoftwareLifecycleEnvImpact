<script lang="ts">
	import type { AggregatedImpact } from 'src/model/impact';
	import type { ResourcesImpact } from 'src/model/taskImpact';

	import ImpactByIndicator from './ImpactByIndicator.svelte';

	export let impactByResource: ResourcesImpact;
	let entries: [string, AggregatedImpact][];

	function updateValues() {
		if (impactByResource != undefined) {
			entries = Object.entries(impactByResource);
		}
	}
	$: impactByResource, updateValues();
</script>

{#if impactByResource != undefined}
	<ul>
		{#each entries as [key, value]}
			<li>
				{key}
				<ImpactByIndicator impact={value} />
			</li>
		{/each}
	</ul>
{/if}
