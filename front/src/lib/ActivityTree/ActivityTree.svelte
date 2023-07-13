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
	import { getModelActivitiesRequest } from '$lib/api/model';
	import ActivityComponent from '$lib/Activity/Activity.svelte';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import type { Model, Activity } from '$lib/api/dataModel';

	/*Bound vars*/
	export let selectedModel: Model;
	export let selectedActivity: Activity;

	let modify = false; // true if modifications are allowed (when "editing mode" is checked)
	let rootActivityPromise: Promise<Activity>;

	/*Trigger update when selected model is updated*/
	$: selectedModel, updateTree();

	async function updateTree() {
		modify = false;
		if (selectedModel != undefined) {
			rootActivityPromise = getModelActivitiesRequest(selectedModel.id).then((res) => {
				/* Switch on modify if ther is no activity in the model*/
				if (res.subactivities.length === 0) {
					modify = true;
				}
				return res;
			});
		}
	}
</script>

{#await rootActivityPromise}
	<Spinner />
{:then rootActivity}
	{#if selectedModel == undefined}
		No model selected
	{:else if rootActivity != undefined}
		<!-- <Header bind:modify bind:selectedActivity {selectedModel} /> -->

		<div class="row sticky-top">
			<div class="col-8">
				<h2 class="title">Activities</h2>
			</div>
			<div class="col-4 form-switch">
				<input class="form-check-input" type="checkbox" bind:checked={modify} id="editmodeSwitch" />
				<label class="form-check-label" for="editmodeSwitch">Editing mode</label>
			</div>
		</div>

		<div
			on:click|stopPropagation={() => (selectedActivity = selectedModel.root_activity)}
			class="card bg-light {selectedModel.root_activity === selectedActivity ? 'border-primary' : ''}"
			style="min-width: 15rem; width: fit-content;"
		>
			<div class="card-body">
				<h5>{selectedModel.name}</h5>
			</div>
		</div>
		<div class="col scroll">
			<ActivityComponent activity={rootActivity} bind:selectedActivity {modify} {selectedModel} parentActivity={rootActivity} />
		</div>
	{/if}
{:catch error}
	<Error message={error.message} />
{/await}
