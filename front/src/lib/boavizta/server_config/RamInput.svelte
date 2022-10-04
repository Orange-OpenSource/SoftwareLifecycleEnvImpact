<script lang="ts">
	import { getRamManufacturers } from '$lib/boavizta/api/ram';
	import type { Ram } from '$lib/boavizta/api/model/ram';

	export let ram: Ram = {};

	const ramManufacturers = getRamManufacturers();
</script>

{#await ramManufacturers}
	<div class="spinner-border" role="status" />
{:then manufacturers}
	<div class="form-group row">
		<div class="form-group col">
			<label for="ramQuantity">Size</label>
			<input
				bind:value={ram.capacity}
				class="form-control"
				type="number"
				id="ramQuantity"
				min="4"
				max="1000"
				step="2"
			/>
		</div>
		<div class="form-group col">
			<label for="ramManufacturer">Manufacturer</label>
			<select bind:value={ram.manufacturer} class="form-control" id="ramManufacturer">
				<option value="" selected class="form-check-input">Unknown</option>
				{#each manufacturers as manufacturer}
					<option value={manufacturer}>
						{manufacturer}
					</option>
				{/each}
			</select>
		</div>

		<div class="form-group col">
			<label for="ramQuantity">Units</label>
			<input bind:value={ram.units} class="form-control" type="number" min="1" max="100" />
		</div>
	</div>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
