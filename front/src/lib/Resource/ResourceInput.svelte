<script lang="ts">
	import type { Resource } from '$lib/api/dataModel';
	import { updateResourceInputRequest } from '$lib/api/resource';
	import Error from '$lib/Error.svelte';
	import TimeunitInput from './TimeunitInput.svelte';

	/*Bound var*/
	export let resource: Resource;

	export let modify: boolean;
	let error = '';

	let timeUseValue: number;
	let timeUseUnit: string;

	let frequencyValue: number;
	let frequencyUnit: string;

	let durationValue: number;
	let durationUnit: string;

	$: frequencyRequired =
		(resource.has_time_input && resource.time_use && resource.time_use.unit != undefined) || (!resource.has_time_input && resource.duration && resource.duration.value != undefined);
	$: durationRequired = resource.has_time_input || (!resource.has_time_input && resource.frequency && resource.frequency.value != undefined);

	$: if (timeUseValue == 0) {
		timeUseValue = undefined;
	}

	$: if (frequencyValue == 0) {
		frequencyValue = undefined;
	}

	$: if (durationValue == 0) {
		durationValue = undefined;
	}

	$: {
		if (!resource.time_use) {
			resource.time_use = {
				value: timeUseValue,
				unit: timeUseUnit
			};
		} else {
			resource.time_use.value = timeUseValue;
			resource.time_use.unit = timeUseUnit;
		}
	}

	$: {
		if (!resource.frequency) {
			resource.frequency = {
				value: frequencyValue,
				unit: frequencyUnit
			};
		} else {
			resource.frequency.value = frequencyValue;
			resource.frequency.unit = frequencyUnit;
		}
	}

	$: {
		if (!resource.duration) {
			resource.duration = {
				value: durationValue,
				unit: durationUnit
			};
		} else {
			resource.duration.value = durationValue;
			resource.duration.unit = durationUnit;
		}
	}
	async function updateResource() {
		try {
			await updateResourceInputRequest(resource);
		} catch (e: any) {
			error = e.message;
		}
	}

	function handleSubmit() {
		updateResource();
	}

	function getText() {
		let test = resource.input.value + ' ' + resource.input.unit + '(s)';
		if (resource.time_use && resource.time_use.value != undefined) test += ', ' + resource.time_use.value + ' ' + resource.time_use.unit + '(s)';
		if (resource.frequency && resource.frequency.value != undefined) test += ' by ' + resource.frequency.value + ' ' + resource.frequency.unit + '(s)';
		if (resource.duration && resource.duration.value != undefined) test += ' for ' + resource.duration.value + ' ' + resource.duration.unit + '(s)';
		return test;
	}
</script>

{#if !modify}
	<p class="card-text">
		{getText()}
	</p>
{:else}
	<form class="card-text needs-validation" novalidate on:submit|preventDefault={handleSubmit}>
		<div class="row">
			<div class="col col-sm-2 col-form-label">
				<div class="form-label is-required">{resource.input.unit}:</div>
			</div>
			<div class="col-sm-10">
				<!-- <label for="inputValue" class="form-label is-required">Value:</label> -->
				<input type="number" id="inputValue" class="form-control" bind:value={resource.input.value} required min="0" on:click|stopPropagation={() => {}} />
			</div>
		</div>
		{#if resource.has_time_input}
			<div class="row">
				<div class="col-sm-2 col-form-label">
					<div class="form-label">Used:</div>
				</div>
				<div class="col-sm-5">
					<input type="number" id="timeUseValue" class="form-control" bind:value={timeUseValue} on:click|stopPropagation={() => {}} />
				</div>
				<div class="col-sm-5">
					<TimeunitInput bind:inputUnit={timeUseUnit} isRequired={false} />
				</div>
			</div>
		{/if}
		<div class="row">
			<!-- <label for="frequencyValue" class="form-label {frequencyRequired() ? 'is-required' : ''}">Frequency:</label> -->
			<div class="col-sm-2 col-form-label">
				<div class="form-label {frequencyRequired ? 'is-required' : ''}">By:</div>
			</div>

			<div class="col-sm-5">
				<input type="number" id="frequencyValue" class="form-control" bind:value={frequencyValue} required={frequencyRequired} min="0" on:click|stopPropagation={() => {}} />
			</div>
			<div class="col-sm-5">
				<TimeunitInput bind:inputUnit={frequencyUnit} isRequired={frequencyRequired} />
			</div>
		</div>
		<div class="row">
			<div class="col col-sm-2 col-form-label">
				<div class="form-label {durationRequired ? 'is-required' : ''}">For:</div>
			</div>
			<div class="col-sm-5">
				<!-- <label for="durationValue" class="form-label {durationRequired() ? 'is-required' : ''}">Duration:</label> -->
				<input type="number" id="durationValue" class="form-control" bind:value={durationValue} required={durationRequired} min="0" on:click|stopPropagation={() => {}} />
			</div>
			<div class="col-sm-5">
				<TimeunitInput bind:inputUnit={durationUnit} isRequired={durationRequired} />
			</div>
		</div>
		<button type="submit" class="btn btn-primary">Submit</button>
	</form>
{/if}

{#if error}
	<Error message={error} />
{/if}
