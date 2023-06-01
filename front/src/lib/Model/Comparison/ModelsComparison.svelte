<script lang="ts">
	import type { Model } from '$lib/api/dataModel';
	import GroupedBarChart from '$lib/Dataviz/GroupedBarChart.svelte';
	import Impact from '$lib/Impact/Impact.svelte';
	import ImpactComparison from '$lib/Impact/ImpactComparison.svelte';

	export let models: Model[];

	let selectedImpactCategory = 'Climate change';
</script>

<div class="row">
	<ImpactComparison {models} bind:selectedImpactCategory />
</div>

<div class="row">
	{#each models as model}
		<div class="col">
			<Impact bind:selectedImpactCategory selectedActivity={model.root_activity} showImpactCategorySelector={false} />
		</div>
	{/each}
</div>
