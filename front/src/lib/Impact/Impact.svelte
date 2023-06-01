<script lang="ts">
	import ImpactBySubactivity from './ImpactBySubactivity.svelte';
	import ImpactBySource from './ImpactBySource.svelte';
	import { getActivityImpact } from '$lib/api/activity';
	import type { ActivityImpact, Activity } from '$lib/api/dataModel';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import ImpactComplete from './ImpactComplete.svelte';

	/*Bound var*/
	export let selectedActivity: Activity;
	let olderActivity: Activity;

	let impactPromise: Promise<ActivityImpact>;
	export let selectedImpactCategory = 'Climate change';
	export let showImpactCategorySelector = true;

	/*Trigger update when selected activity is updated*/
	$: selectedActivity, updateImpacts();

	function updateImpacts() {
		// WIthout this, sometimes the selectedActivity refresh was called indefinitely
		if (selectedActivity != undefined && (olderActivity == undefined || olderActivity != selectedActivity)) {
			olderActivity = selectedActivity;
			impactPromise = getActivityImpact(selectedActivity);
		}
	}
</script>

<div class="col-md-auto">
	{#if selectedActivity != undefined}
		{#await impactPromise}
			<Spinner />
		{:then impact}
			{#if impact != undefined && Object.keys(impact.impact_sources).length}
				<div class="row">
					<h1 class="text-primary">{selectedActivity.name}</h1>
				</div>
				{#if showImpactCategorySelector}
					<div class="d-flex">
						<select class="form-select" bind:value={selectedImpactCategory} required>
							{#each Object.entries(impact.total) as [key, _]}
								<option value={key} class="form-check-input">{key}</option>
							{/each}
						</select>
					</div>
				{/if}
				{#if impact.sub_activities.length > 0}
					<div class="row">
						<ImpactComplete bind:selectedActivity {impact} {selectedImpactCategory} />
					</div>
					<div class="row">
						<ImpactBySubactivity bind:selectedActivity {impact} {selectedImpactCategory} />
					</div>
				{/if}
				<div class="row">
					<ImpactBySource bind:selectedActivity {impact} {selectedImpactCategory} />
				</div>
			{:else}
				No impact
			{/if}
		{:catch error}
			<Error message={error.message} />
		{/await}
	{:else}
		No element selected
	{/if}
</div>
