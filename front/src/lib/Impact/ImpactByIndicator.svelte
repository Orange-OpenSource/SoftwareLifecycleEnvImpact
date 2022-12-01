<script lang="ts">
	import type { EnvironmentalImpact } from '$lib/api/dataModel';

	export let environmentalImpact: EnvironmentalImpact;
</script>

{#if environmentalImpact != undefined}
	<ul>
		{#each Object.entries(environmentalImpact.impacts) as [key, impact]}
			{#if impact.value != 0}
				<li>
					{key}: <b>{Math.round(impact.value * 100) / 100}</b>
					{impact.unit}
				</li>
			{/if}
		{/each}
	</ul>
{/if}
