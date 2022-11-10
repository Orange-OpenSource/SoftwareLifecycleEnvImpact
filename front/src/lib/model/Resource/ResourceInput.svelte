<script lang="ts">
	import Error from '$lib/Error.svelte';
	import { TIME_UNITS, type Resource } from '../api/model/resource';
	import { updateResourceInputRequest } from '../api/resource';
	import TimeunitInput from './TimeunitInput.svelte';

	/*Bound var*/
	export let resource: Resource;

	export let modify: boolean;
	let error = '';

	async function updateResource() {
		try {
			await updateResourceInputRequest(resource);
		} catch (e: any) {
			error = e.message;
		}
	}

	function getDuration() {
		// let duration = 'for ';
		// if (resource.days) duration += resource.days + (resource.days > 1 ? ' days,' : ' day,');
		// if (resource.months) duration += resource.months + (resource.months > 1 ? ' months,' : ' month,');
		// if (resource.years) duration += resource.years + (resource.years > 1 ? ' years,' : ' year,');
		// if (duration == 'for ') return '';
		// return duration.replace(/,$/, ''); // Remove trailing , if it exists
		return 'todo getDuration'; // TODO
	}
</script>

{#if !modify}
	<p class="card-text">
		{resource.input}
		{resource.impact_source_id}
		{getDuration()}
	</p>
{:else}
	<form class="card-text">
		<div class="row">
			<div class="col">
				<label for="inputValue" class="form-label">{resource.input.unit}:</label>
				<input type="number" id="inputValue" class="form-control" bind:value={resource.input.value} min="1" on:change={() => updateResource()} on:click|stopPropagation={() => {}} />
			</div>
		</div>
		{#if resource.time_use}
			<div class="row">
				<div class="col">
					<label for="timeUseValue" class="form-label">Time use:</label>
					<input type="number" id="timeUseValue" class="form-control" bind:value={resource.time_use.value} min="1" on:change={() => updateResource()} on:click|stopPropagation={() => {}} />
				</div>
				<div class="col">
					<TimeunitInput bind:inputUnit={resource.time_use.unit} />
				</div>
			</div>
		{/if}
		{#if resource.frequency}
			<div class="row">
				<div class="col">
					<label for="frequencyValue" class="form-label">Frequency:</label>
					<input type="number" id="frequencyValue" class="form-control" bind:value={resource.frequency.value} min="1" on:change={() => updateResource()} on:click|stopPropagation={() => {}} />
				</div>
				<div class="col">
					<TimeunitInput bind:inputUnit={resource.frequency.unit} />
				</div>
			</div>
		{/if}
		{#if resource.duration}
			<div class="row">
				<div class="col">
					<label for="durationValue" class="form-label">Duration:</label>
					<input type="number" id="durationValue" class="form-control" bind:value={resource.duration.value} min="1" on:change={() => updateResource()} on:click|stopPropagation={() => {}} />
				</div>
				<div class="col">
					<TimeunitInput bind:inputUnit={resource.duration.unit} />
				</div>
			</div>
		{/if}
	</form>
{/if}

{#if error}
	<Error message={error} />
{/if}
