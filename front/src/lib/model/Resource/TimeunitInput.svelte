<script lang="ts">
	import { TIME_UNITS } from '../api/model/resource';

	/*Bound var*/
	export let inputUnit: string;
</script>

<label for="inputUnit" class="form-label">Unit:</label>
<select bind:value={inputUnit} class="form-control" id="inputUnit">
	{#each TIME_UNITS as unit}
		<option value={unit}>
			{unit}
		</option>
	{/each}
</select>
