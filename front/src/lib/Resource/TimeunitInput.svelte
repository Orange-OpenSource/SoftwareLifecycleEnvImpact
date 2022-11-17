<script lang="ts">
	import { TIME_UNITS } from "$lib/api/dataModel";




	/*Bound var*/
	export let inputUnit: string;

	export let isRequired: boolean;
</script>

<!-- <label for="inputUnit" class="form-label {isRequired ? 'is-required' : ''}">Unit:</label> -->
<select bind:value={inputUnit} class="form-control" id="inputUnit" required={isRequired}>
	<option />
	{#each TIME_UNITS as unit}
		<option value={unit}>
			{unit}
		</option>
	{/each}
</select>
