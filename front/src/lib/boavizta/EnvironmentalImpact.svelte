<script lang="ts">
	import type { ServerImpact } from './model/serverImpact';
	import Impact from './Impact.svelte';

	export let impact: Promise<ServerImpact>;
</script>

{#await impact}
	<div class="spinner-border" role="status" />
{:then loadedImpact}
	{#if loadedImpact != undefined}
		<ul>
			<li>
				<b>Global Warming Potential</b>
				<Impact impact={loadedImpact.impacts.gwp} />
			</li>
			<li>
				<b>Abiotic Depletion Potential</b>
				<Impact impact={loadedImpact.impacts.adp} />
			</li>

			<li>
				<b>Primary Energy</b>
				<Impact impact={loadedImpact.impacts.pe} />
			</li>
		</ul>
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
