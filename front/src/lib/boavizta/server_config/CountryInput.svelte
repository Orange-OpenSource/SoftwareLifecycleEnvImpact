<script lang="ts">
	import { getCountries } from '$lib/boavizta/api/countries';

	export let country = '';

	const countries = getCountries();
</script>

{#await countries}
	<div class="spinner-border" role="status" />
{:then infos}
	<div class="form-group row">
		<label for="cpuFamilies">Country</label>
		<select bind:value={country} class="form-control" id="cpuFamilies">
			<option value="" selected class="form-check-input">Unknown</option>
			{#each infos as [key, value]}
				<option {value}>
					{key}
				</option>
			{/each}
		</select>
	</div>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
