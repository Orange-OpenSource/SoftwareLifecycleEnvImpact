<script lang="ts">
	import type { Resource } from '$lib/api/dataModel';
	import { renameResourceRequest, updateResourceInputRequest } from '$lib/api/resource';
	import Error from '$lib/Error.svelte';
	import TimeunitInput from './TimeunitInput.svelte';

	/*Bound var*/
	export let resource: Resource;
	export let modify: boolean;

	let errors: { [key: string]: string } = {};

	// undefined values cannot be bind to html elements
	$: if (resource.duration == undefined) resource.duration = {};
	$: if (resource.frequency == undefined) resource.frequency = {};
	$: if (resource.time_use == undefined) resource.time_use = {};

	// Clear duration quantity values when setting field to 0
	$: if (resource.duration != undefined && resource.duration.value == 0) {
		resource.duration.value = undefined;
		resource.duration.unit = undefined;
	}
	$: if (resource.frequency != undefined && resource.frequency.value == 0) {
		resource.frequency.value = undefined;
		resource.frequency.unit = undefined;
	}
	$: if (resource.time_use != undefined && resource.time_use.value == 0) {
		resource.time_use.value = undefined;
		resource.time_use.unit = undefined;
	}

	// Helpers bool with logic if frequency or duration field are required
	$: frequencyRequired = (resource.has_time_input && resource.time_use.unit != undefined) || (!resource.has_time_input && resource.duration.value != undefined);
	$: durationRequired = resource.has_time_input || (!resource.has_time_input && resource.frequency.value != undefined);

	// Clean error message when modify eddit button is untriggered
	$: modify, cleanError();
	function cleanError() {
		if (!modify) errors = {};
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
		if (resource.time_use.value != undefined) test += ', ' + resource.time_use.value + ' ' + resource.time_use.unit + '(s)';
		if (resource.frequency.value != undefined) test += ' by ' + resource.frequency.value + ' ' + resource.frequency.unit + '(s)';
		if (resource.duration.value != undefined) test += ' for ' + resource.duration.value + ' ' + resource.duration.unit + '(s)';
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
					<input type="number" id="timeUseValue" class="form-control {errors.time_use ? 'is-invalid' : ''}" min="0" bind:value={resource.time_use.value} on:click|stopPropagation={() => {}} />
				</div>
				<div class="col-sm-5">
					<TimeunitInput bind:inputUnit={resource.time_use.unit} isRequired={false} isInvalid={errors.time_use} />
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
				<div class="form-label {durationRequired ? 'is-required' : ''}">For:</div>
			</div>
			<div class="col-sm-5">
				<!-- <label for="durationValue" class="form-label {durationRequired() ? 'is-required' : ''}">Duration:</label> -->
				<input type="number" id="durationValue" class="form-control" bind:value={resource.duration.value} required={durationRequired} min="0" on:click|stopPropagation={() => {}} />
			</div>
			<div class="col-sm-5">
				<TimeunitInput bind:inputUnit={resource.duration.unit} isRequired={durationRequired} />
			</div>
		</div>
		{#each errors.generic || [] as error}
			<Error message={error} />
		{/each}
		<button type="submit" class="btn btn-primary">Submit</button>
	</form>
{/if}
