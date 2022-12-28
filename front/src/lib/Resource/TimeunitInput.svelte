<script lang="ts">
	import { TIME_UNITS } from '$lib/api/dataModel';

	/*Bound var*/
	export let inputUnit: string | undefined;

	export let isRequired: boolean;
	export let isInvalid: any;

	// Copy object to split unit string with businessDay boolean
	let inputUnitLayout = inputUnit?.replace('business_', '');
	let businessDay = inputUnit?.includes('business_');

	// Update inputUnit with business_ prefix or not following checkbox value
	$: inputUnit = businessDay ? 'business_' + inputUnitLayout : inputUnitLayout;
</script>

<select bind:value={inputUnitLayout} class="form-control {isInvalid ? 'is-invalid' : ''}" id="inputUnit" required={isRequired}>
	<option />
	{#each TIME_UNITS as unit}
		<option value={unit}>
			{unit}
		</option>
	{/each}
</select>
<!-- Only display for week month or year -->
{#if inputUnitLayout == 'week' || inputUnitLayout == 'month' || inputUnitLayout == 'year'}
	<div class="form-check">
		<input class="form-check-input" type="checkbox" bind:checked={businessDay} id="timeInputBusiness" />
		<label class="form-check-label" for="timeInputBusiness">Business day</label>
	</div>
{/if}
