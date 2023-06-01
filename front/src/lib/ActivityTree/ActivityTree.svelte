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
