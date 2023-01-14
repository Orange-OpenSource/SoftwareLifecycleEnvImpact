<script lang="ts">
	import type { Resource } from '$lib/api/dataModel';
	import { updateResourceAmountRequest } from '$lib/api/resource';
	import Error from '$lib/Error.svelte';
	import TimeunitInput from './TimeunitInput.svelte';

	/*Bound var*/
	export let resource: Resource;
	export let modify: boolean;

	let errors: { [key: string]: string } = {};

	// undefined values cannot be bind to html elements
	$: if (resource.period == undefined) resource.period = {};
	$: if (resource.frequency == undefined) resource.frequency = {};
	$: if (resource.duration == undefined) resource.duration = {};

	// Clear period quantity values when setting field to 0
	$: if (resource.period != undefined && resource.period.value == 0) {
		resource.period.value = undefined;
		resource.period.unit = undefined;
	}
	$: if (resource.frequency != undefined && resource.frequency.value == 0) {
		resource.frequency.value = undefined;
		resource.frequency.unit = undefined;
	}
	$: if (resource.duration != undefined && resource.duration.value == 0) {
		resource.duration.value = undefined;
		resource.duration.unit = undefined;
	}

	// Helpers bool with logic if frequency or period field are required
	// Duration is required if has time and frequency is filled
	$: durationRequired = resource.has_time_input && resource.frequency.value != undefined;

	// Frequency is required if time in impact source and duration filled, or if no time if period is filled
	$: frequencyRequired = (resource.has_time_input && resource.duration.value != undefined) || (!resource.has_time_input && resource.period.value != undefined);

	// Period is required if time in impact source, of if not and frequency is set
	$: periodRequired = resource.has_time_input || (!resource.has_time_input && resource.frequency.value != undefined);

	// Clean error message when modify eddit button is untriggered
	$: modify, cleanError();
	function cleanError() {
		if (!modify) errors = {};
	}

	async function updateResource() {
		try {
			//reset errors
			errors = {};
			resource = await updateResourceAmountRequest(resource);
		} catch (e: any) {
			errors = e.errors;
		}
	}

	function handleSubmit() {
		updateResource();
	}

	function getText() {
		let test = resource.amount.value + ' ' + resource.amount.unit + (resource.amount.value && resource.amount.value > 1 ? 's' : '');
		if (resource.duration.value != undefined) test += ', ' + resource.duration.value + ' ' + resource.duration.unit + (resource.duration.value > 1 ? 's' : '');
		if (resource.frequency.value != undefined) test += ' by ' + resource.frequency.value + ' ' + resource.frequency.unit + (resource.frequency.value > 1 ? 's' : '');
		if (resource.period.value != undefined) test += ' for ' + resource.period.value + ' ' + resource.period.unit + (resource.period.value > 1 ? 's' : '');
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
				<div class="form-label is-required">{resource.amount.unit}:</div>
			</div>
			<div class="col-sm-10">
				<!-- <label for="amountValue" class="form-label is-required">Value:</label> -->
				<input
					type="number"
					step="0.1"
					id="amountValue"
					class="form-control {errors.amount ? 'is-invalid' : ''}"
					bind:value={resource.amount.value}
					required
					min="1"
					on:click|stopPropagation={() => {}}
				/>
			</div>
			{#each errors.amount || [] as error}
				<div class="invalid-feedback"><Error message={error} /></div>
			{/each}
		</div>
		{#if resource.has_time_input}
			<div class="row">
				<div class="col-sm-2 col-form-label {durationRequired ? 'is-required' : ''}">
					<div class="form-label">Used:</div>
				</div>
				<div class="col-sm-5">
					<input type="number" id="timeUseValue" class="form-control {errors.duration ? 'is-invalid' : ''}" min="0" bind:value={resource.duration.value} on:click|stopPropagation={() => {}} />
				</div>
				<div class="col-sm-5">
					<TimeunitInput bind:inputUnit={resource.duration.unit} isRequired={durationRequired} isInvalid={errors.duration} />
				</div>
				{#if errors.duration}
					<!-- Quantity errors -->
					{#if errors.duration._schema}
						<Error message={errors.duration._schema} />
					{:else}
						<!-- Logic error -->
						{#each errors.duration || [] as error}
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
					bind:value={resource.frequency.value}
					required={frequencyRequired}
					min="0"
					on:click|stopPropagation={() => {}}
				/>
			</div>
			<div class="col-sm-5">
				<TimeunitInput bind:inputUnit={resource.frequency.unit} isRequired={frequencyRequired} isInvalid={errors.frequency} />
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
				<div class="form-label {periodRequired ? 'is-required' : ''}">For:</div>
			</div>
			<div class="col-sm-5">
				<!-- <label for="periodValue" class="form-label {periodRequired() ? 'is-required' : ''}">Period:</label> -->
				<input type="number" id="periodValue" class="form-control" bind:value={resource.period.value} required={periodRequired} min="0" on:click|stopPropagation={() => {}} />
			</div>
			<div class="col-sm-5">
				<TimeunitInput bind:inputUnit={resource.period.unit} isRequired={periodRequired} />
			</div>
		</div>
		{#each errors.generic || [] as error}
			<Error message={error} />
		{/each}
		<button type="submit" class="btn btn-primary">Submit</button>
	</form>
{/if}
