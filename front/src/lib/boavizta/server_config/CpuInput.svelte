<script lang="ts">
	import { getCpuInfos } from '$lib/boavizta/api/cpu';
	import type { Cpu } from '$lib/boavizta/api/model/cpu';

	export let cpu: Cpu = {};

	const cpuInfos = getCpuInfos();
</script>

{#await cpuInfos}
	<div class="spinner-border" role="status" />
{:then infos}
	<div class="form-group row">
		<div class="form-group col">
			<label for="cpuModel">Model</label>
			<select bind:value={cpu.model} class="form-control" id="cpuModel">
				<option value="" selected class="form-check-input">Unknown</option>
				{#each infos.models as model}
					<option value={model}>
						{model}
					</option>
				{/each}
			</select>
		</div>

		<div class="form-group col">
			<div class="row">
				<div class="col">
					<label for="cpuFamilies">Family</label>
					<select bind:value={cpu.family} class="form-control" id="cpuFamilies">
						<option value="" selected class="form-check-input">Unknown</option>
						{#each infos.families as family}
							<option value={family}>
								{family}
							</option>
						{/each}
					</select>
				</div>

				<div class="col">
					<label for="coreNumbers">Cores</label>
					<input
						bind:value={cpu.core_units}
						type="number"
						id="coreNumbers"
						min="1"
						max="50"
						class="form-control"
					/>
				</div>
			</div>
		</div>

		<div class="form-group col">
			<label for="ramQuantity">Units</label>
			<input bind:value={cpu.units} class="form-control" type="number" min="1" max="10" />
		</div>
	</div>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
