<script lang="ts">
	import { getDiskManufacturers } from '../api/disk';
	import type { Disk } from '../api/model/disk';

	export let disks: Disk[] = [{}];

	const diskManufacturers = getDiskManufacturers();

	function addDisk() {
		disks.push({});
		disks = disks;
		/*Redondant assignment to force Svelte to update components*/
	}

	function deleteDisk(disk: Disk) {
		const index = disks.indexOf(disk);
		if (index > -1) {
			// Find index of disk in array then remove it
			disks.splice(index, 1);
		}
		disks = disks;
		/*Redondant assignment to force Svelte to update components*/
	}
</script>

{#await diskManufacturers}
	<div class="spinner-border" role="status" />
{:then manufacturers}
	{#each disks as disk}
		<div class="form-group row">
			<div class="form-group col">
				<label for="diskCapacity">Capacity (GB)</label>
				<input bind:value={disk.capacity} type="number" class="form-control" id="diskCapacity" min="10" max="10000" step="10" />
			</div>

			<div class="form-group col ">
				<label for="diskType">Type</label>
				<select bind:value={disk.type} class="form-control" id="ramManufacturer">
					<option value="" selected class="form-check-input">Unknown</option>
					<option value="ssd"> SSD </option>
					<option value="hdd"> HDD </option>
				</select>
			</div>

			<div class="form-group col">
				<label for="diskManufacturer">Manufacturer</label>
				<select bind:value={disk.manufacturer} class="form-control" id="diskManufacturer">
					<option value="" selected class="form-check-input">Unknown</option>
					{#each manufacturers as manufacturer}
						<option value={manufacturer}>
							{manufacturer}
						</option>
					{/each}
				</select>
			</div>

			{#if disks.length > 1}
				<div class="col">
					<button type="button" class="btn btn-danger" on:click={deleteDisk(disk)}>Delete</button>
				</div>
			{/if}
		</div>
	{/each}
	<button type="button" class="btn btn-secondary" on:click={addDisk}>Add disk</button>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
