<script lang="ts">
	import type { EnvironmentalImpact } from '$lib/api/model/impacts';

	export let environmentalImpact: EnvironmentalImpact;
</script>

{#if environmentalImpact != undefined}
	<ul>
		{#each Object.entries(environmentalImpact.impacts) as [key, impact]}
			{#if impact.value != 0}
				<li>
					{key}: <b>{impact.value}</b>
					{impact.unit}
				</li>
			{/if}
		{/each}
	</ul>
{/if}
