<script lang="ts">
	import Error from '$lib/Error.svelte';
	import type { Resource } from '../api/model/resource';
	import { updateResourceInputRequest } from '../api/resource';

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
		let duration = 'for ';
		if (resource.days) duration += resource.days + (resource.days > 1 ? ' days,' : ' day,');
		if (resource.months) duration += resource.months + (resource.months > 1 ? ' months,' : ' month,');
		if (resource.years) duration += resource.years + (resource.years > 1 ? ' years,' : ' year,');
		if (duration == 'for ') return '';
		return duration.replace(/,$/, ''); // Remove trailing , if it exists
	}
</script>

{#if !modify}
	<p class="card-text">
		{resource.input}
		{resource.impact_source_name}
		{getDuration()}
	</p>
{:else}
	<form class="card-text">
		<div class="row">
			<div class="col">
				<label for="inputValue" class="form-label">{resource.impact_source_name}:</label>
				<input type="number" id="inputValue" class="form-control" bind:value={resource.input} min="1" on:change={() => updateResource()} on:click={() => {}} />
			</div>
		</div>
		<div class="row">
			<div class="col">
				<label for="inputDays" class="form-label">Days:</label>
				<input type="number" id="inputDays" class="form-control" bind:value={resource.days} min="0" on:change={() => updateResource()} on:click={() => {}} />
			</div>
			<div class="col">
				<label for="inputMonths" class="form-label">Months:</label>
				<input type="number" id="inputMonths" class="form-control" bind:value={resource.months} min="0" on:change={() => updateResource()} on:click={() => {}} />
			</div>
			<div class="col">
				<label for="inputYears" class="form-label">Years:</label>
				<input type="number" id="inputYears" class="form-control" bind:value={resource.years} min="0" on:change={() => updateResource()} on:click={() => {}} />
			</div>
		</div>
	</form>
{/if}

{#if error}
	<Error message={error} />
{/if}
