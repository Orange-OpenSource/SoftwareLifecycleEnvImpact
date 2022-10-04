<script lang="ts">
	import { getServerImpactByConfig } from '$lib/boavizta/api/server';
	import EnvironmentalImpact from '$lib/boavizta/EnvironmentalImpact.svelte';
	import ImpactByComponent from '$lib/boavizta/ImpactByComponent.svelte';
	import type { ConfigurationServer } from '$lib/boavizta/api/model/configurationServer';
	import type { ServerImpact } from '$lib/boavizta/api/model/serverImpact';
	import type { UsageServer } from '$lib/boavizta/api/model/usageServer';
	import CountryInput from './CountryInput.svelte';
	import CpuInput from './CpuInput.svelte';
	import DisksInput from './DisksInput.svelte';
	import PowerSupplyInput from './PowerSupplyInput.svelte';
	import RamInput from './RamInput.svelte';

	let config: ConfigurationServer = {};
	config.ram = new Array();
	let usage: UsageServer = {};
	let impact: Promise<ServerImpact>;

	function handleSubmit() {
		impact = getServerImpactByConfig(config, usage);
	}
</script>

<div class="row">
	<div class="col-9">
		<h1>Configuration</h1>
		<form on:submit|preventDefault={handleSubmit}>
			<div class="accordion">
				<div class="accordion-item">
					<h2 class="accordion-header">
						<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseCPU"> CPU </button>
					</h2>
					<div id="collapseCPU" class="accordion-collapse collapse show">
						<div class="accordion-body">
							<CpuInput bind:cpu={config.cpu} />
						</div>
					</div>
				</div>

				<div class="accordion-item">
					<h2 class="accordion-header">
						<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseRAM"> RAM </button>
					</h2>
					<div id="collapseRAM" class="accordion-collapse collapse show">
						<div class="accordion-body">
							<RamInput bind:ram={config.ram[0]} />
						</div>
					</div>
				</div>

				<div class="accordion-item">
					<h2 class="accordion-header">
						<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseDisk"> Disk </button>
					</h2>
					<div id="collapseDisk" class="accordion-collapse collapse show">
						<div class="accordion-body">
							<DisksInput bind:disks={config.disk} />
						</div>
					</div>
				</div>

				<div class="accordion-item">
					<h2 class="accordion-header">
						<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapsePS"> Power supply </button>
					</h2>
					<div id="collapsePS" class="accordion-collapse collapse show">
						<div class="accordion-body">
							<PowerSupplyInput bind:power_supply={config.power_supply} />
						</div>
					</div>
				</div>

				<div class="accordion-item">
					<h2 class="accordion-header">
						<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseCountry"> Country </button>
					</h2>
					<div id="collapseCountry" class="accordion-collapse collapse show">
						<div class="accordion-body">
							<CountryInput bind:country={usage.usage_location} />
						</div>
					</div>
				</div>
			</div>

			<button type="submit" class="btn btn-primary">Compute</button>
		</form>
	</div>
	<div class="col-3">
		<h1>Environmental impact</h1>
		<EnvironmentalImpact {impact} />

		<h2>Fabrication 🔨</h2>
		<ImpactByComponent {impact} />
	</div>
</div>
