<script lang="ts">
	import type { ResourceInput } from '$lib/model/api/model/resource';
	import { updateResourceInputRequest } from '../api/resource_input';
	import Error from '$lib/Error.svelte';

	/*Bound var*/
	export let resourceInput: ResourceInput;

	export let modify: boolean;
	let error = '';

	async function updateResource() {
		try {
			await updateResourceInputRequest(resourceInput);
		} catch (e: any) {
			error = e.message;
		}
	}

	function getDuration() {
		let duration = 'for ';
		if (resourceInput.days) duration += resourceInput.days + ' day(s),';
		if (resourceInput.months) duration += resourceInput.months + ' month(s),';
		if (resourceInput.years) duration += resourceInput.years + ' year(s),';
		if (duration == 'for ') return '';
		return duration.replace(/,$/, ''); // Remove trailing , if it exists
	}
</script>

{#if !modify}
	<p class="card-text">
		{resourceInput.input}
		{resourceInput.type}
		{getDuration()}
	</p>
{:else}
	<form class="card-text">
		<div class="row">
			<div class="col">
				<label for="inputValue" class="form-label">{resourceInput.type}:</label>
				<input type="number" id="inputValue" class="form-control" bind:value={resourceInput.input} min="1" on:change={() => updateResource()} on:click={() => {}} />
			</div>
		</div>
		<div class="row">
			<div class="col">
				<label for="inputDays" class="form-label">Days:</label>
				<input type="number" id="inputDays" class="form-control" bind:value={resourceInput.days} min="0" on:change={() => updateResource()} on:click={() => {}} />
			</div>
			<div class="col">
				<label for="inputMonths" class="form-label">Months:</label>
				<input type="number" id="inputMonths" class="form-control" bind:value={resourceInput.months} min="0" on:change={() => updateResource()} on:click={() => {}} />
			</div>
			<div class="col">
				<label for="inputYears" class="form-label">Years:</label>
				<input type="number" id="inputYears" class="form-control" bind:value={resourceInput.years} min="0" on:change={() => updateResource()} on:click={() => {}} />
			</div>
		</div>
	</form>
{/if}

{#if error}
	<Error message={error} />
{/if}
