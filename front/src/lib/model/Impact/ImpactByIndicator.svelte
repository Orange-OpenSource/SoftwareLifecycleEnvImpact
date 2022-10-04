<script lang="ts">
	import type { AggregatedImpact } from '$lib/model/api/model/impacts';

	export let impact: AggregatedImpact;
</script>

{#if impact != undefined}
	<ul>
		{#each Object.entries(impact) as [key, impact]}
			{#if impact.value != 0}
				<li>
					{key}: <b>{impact.value}</b>
					{impact.unit}
				</li>
			{/if}
		{/each}
	</ul>
{/if}
