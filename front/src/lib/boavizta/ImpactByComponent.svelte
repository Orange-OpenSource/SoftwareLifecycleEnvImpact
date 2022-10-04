<script lang="ts">
	import type { ServerImpact } from './model/serverImpact';
	import EnvironmentalImpact from './EnvironmentalImpact.svelte';
	export let impact: Promise<ServerImpact>;
</script>

{#await impact}
	<div class="spinner-border" role="status" />
{:then loadedImpact}
	{#if loadedImpact != undefined}
		<h5>Assembly</h5>
		<EnvironmentalImpact impact={loadedImpact.verbose['ASSEMBLY-1']} />

		<h5>CPU</h5>
		<EnvironmentalImpact impact={loadedImpact.verbose['CPU-1']} />

		<h5>RAM</h5>
		<EnvironmentalImpact impact={loadedImpact.verbose['RAM-1']} />

		<h5>Power supply</h5>
		<EnvironmentalImpact impact={loadedImpact.verbose['POWER_SUPPLY-1']} />

		<h5>Case</h5>
		<EnvironmentalImpact impact={loadedImpact.verbose['CASE-1']} />

		<h5>Motherboard</h5>
		<EnvironmentalImpact impact={loadedImpact.verbose['MOTHERBOARD-1']} />

		<h5>Usage</h5>
		<EnvironmentalImpact impact={loadedImpact.verbose['USAGE']} />
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
