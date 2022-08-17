<script lang="ts">
	import type { AggregatedImpact } from 'src/model/impacts';

	export let impact: AggregatedImpact;

	let entries: [string, any][];

	$: impact, updateEntries();

	function updateEntries() {
		if (impact != undefined) {
			entries = Object.entries(impact);
		}
	}
</script>

{#if entries != undefined}
	<ul>
		{#each entries as [key, impact]}
			{#if impact.value != 0}
				<li>
					{key}: <b>{impact.value}</b>
					{impact.unit}
				</li>
			{/if}
		{/each}
	</ul>
{/if}
