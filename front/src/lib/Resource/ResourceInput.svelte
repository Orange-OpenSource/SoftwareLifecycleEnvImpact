<script lang="ts">
	import type { Resource } from '$lib/api/dataModel';
	import { updateResourceInputRequest } from '$lib/api/resource';
	import Error from '$lib/Error.svelte';
	import TimeunitInput from './TimeunitInput.svelte';

	/*Bound var*/
	export let resource: Resource;

	export let modify: boolean;
	let errors: { [key: string]: string } = {};

	let timeUseValue: number;
	let timeUseUnit: string;

	let frequencyValue: number;
	let frequencyUnit: string;

	let durationValue: number;
	let durationUnit: string;

	$: modify, cleanError(); // Clean error message when modify eddit button is untriggered

	function cleanError() {
		if (!modify) errors = {};
	}

	$: frequencyRequired =
		(resource.has_time_input && resource.time_use && resource.time_use.unit != undefined) || (!resource.has_time_input && resource.duration && resource.duration.value != undefined);
	$: durationRequired = resource.has_time_input || (!resource.has_time_input && resource.frequency && resource.frequency.value != undefined);

	$: if (timeUseValue == 0) {
		timeUseValue = undefined;
		timeUseUnit = undefined;
	}

	$: if (frequencyValue == 0) {
		frequencyValue = undefined;
		frequencyUnit = undefined;
	}

	$: if (durationValue == 0) {
		durationValue = undefined;
		durationUnit =  undefined;
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
			//reset errors
			errors = {};
			resource = await updateResourceInputRequest(resource);
		} catch (e: any) {
			errors = e.errors;
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
	<form class="card-text needs-validation" on:submit|preventDefault={handleSubmit}>
		<div class="row">
			<div class="col col-sm-2 col-form-label">
				<div class="form-label is-required">{resource.input.unit}:</div>
			</div>
			<div class="col-sm-10">
				<!-- <label for="inputValue" class="form-label is-required">Value:</label> -->
				<input type="number" id="inputValue" class="form-control {errors.input ? 'is-invalid' : ''}" bind:value={resource.input.value} required min="1" on:click|stopPropagation={() => {}} />
			</div>
			{#each errors.input || [] as error}
				<div class="invalid-feedback"><Error message={error} /></div>
			{/each}
		</div>
		{#if resource.has_time_input}
			<div class="row">
				<div class="col-sm-2 col-form-label">
					<div class="form-label">Used:</div>
				</div>
				<div class="col-sm-5">
					<input type="number" id="timeUseValue" class="form-control {errors.time_use ? 'is-invalid' : ''}" bind:value={timeUseValue} on:click|stopPropagation={() => {}} />
				</div>
				<div class="col-sm-5">
					<TimeunitInput bind:inputUnit={timeUseUnit} isRequired={false} isInvalid={errors.time_use} />
				</div>
				{#if errors.time_use}
					<!-- Quantity errors -->
					{#if errors.time_use._schema}
						<Error message={errors.time_use._schema} />
					{:else}
						<!-- Logic error -->
						{#each errors.time_use || [] as error}
							<Error message={error} />
						{/each}
					{/if}
				{/if}
			</div>
		{/if}
		<div class="row">
			<!-- <label for="frequencyValue" class="form-label {frequencyRequired() ? 'is-required' : ''}">Frequency:</label> -->
			<div class="col-sm-2 col-form-label">
				<div class="form-label {frequencyRequired ? 'is-required' : ''}">By:</div>
			</div>

			<div class="col-sm-5">
				<input
					type="number"
					id="frequencyValue"
					class="form-control {errors.frequency ? 'is-invalid' : ''}"
					bind:value={frequencyValue}
					required={frequencyRequired}
					min="0"
					on:click|stopPropagation={() => {}}
				/>
			</div>
			<div class="col-sm-5">
				<TimeunitInput bind:inputUnit={frequencyUnit} isRequired={frequencyRequired} isInvalid={errors.frequency} />
			</div>
			{#if errors.frequency}
				<!-- Quantity errors -->
				{#if errors.frequency._schema}
					<Error message={errors.frequency._schema} />
				{:else}
					<!-- Logic error -->
					{#each errors.frequency || [] as error}
						<Error message={error} />
					{/each}
				{/if}
			{/if}
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
		{#each errors.generic || [] as error}
			<Error message={error} />
		{/each}
		<button type="submit" class="btn btn-primary">Submit</button>
	</form>
{/if}
