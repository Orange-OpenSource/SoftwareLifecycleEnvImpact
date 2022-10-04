<script lang="ts">
	import type { VerboseImpact } from './model/serverImpact';
	export let impact: VerboseImpact;
</script>

<div>
	{#if impact != undefined}
		{#if impact.value != undefined}
			{impact.value} {impact.unit}
		{:else}
			<ul>
				<li>🔨 {impact.manufacture} {impact.unit}</li>
				<li>🔌 {impact.use} {impact.unit}</li>
			</ul>
		{/if}
	{/if}
</div>
