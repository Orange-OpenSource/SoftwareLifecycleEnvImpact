<!-- BSD 3-Clause License

Copyright (c) 2017, Orange
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. -->
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
