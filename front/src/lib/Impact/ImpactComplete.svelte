<script lang="ts">
	import type { Task, TaskImpact } from '$lib/api/dataModel';
	import { constructLinks, type D3JSLink } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';

	export let impact: TaskImpact;
	export let selectedImpactCategory: string;

	/*Bound var*/
	export let selectedTask: Task;

	$: subtasksLinks = constructLinks(selectedImpactCategory, selectedTask, impact);
</script>

{#if impact.sub_tasks.length > 0}
	<Sankey links={subtasksLinks} />
{/if}
