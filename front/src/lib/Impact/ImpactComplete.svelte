<script lang="ts">
	import type { Activity, ActivityImpact } from '$lib/api/dataModel';
	import { constructLinks, type D3JSLink } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';

	export let impact: ActivityImpact;
	export let selectedImpactCategory: string;

	/*Bound var*/
	export let selectedActivity: Activity;

	$: subactivitiesLinks = constructLinks(selectedImpactCategory, selectedActivity, impact);
</script>

{#if impact.sub_activities.length > 0}
	<Sankey links={subactivitiesLinks} />
{/if}
