<script lang="ts">
	import Modal from '$lib/Modal.svelte';
	import { getImpactSources } from '$lib/model/api/impactSources';
	import type { Task } from '$lib/model/api/model/task';
	import { addResourceRequest } from '$lib/model/api/resource';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import type { ImpactSource } from '../api/model/resource';

	/*Bound var*/
	export let task: Task;

	let showModal = false;

	let impactSourcesPromise = getImpactSources();
	let selectedImpactSource: ImpactSource;
	let name = '';

	let error = '';
	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		name = '';
	}

	async function handleSubmit() { // TODO error marche pas à cause du async
		error = '';
		try {
			if (selectedImpactSource != null) {
				const res = await addResourceRequest(name, task.id, selectedImpactSource);
				task.resources.push(res);
				/*Redondant assignment to force Svelte to update components*/
				task.resources = task.resources;
				showModal = false;
			}
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-link">Add resource</button>

<Modal bind:showModal>
	<span slot="title">Add new resource :</span>
	<form slot="body" on:submit|preventDefault={handleSubmit}>
		{#await impactSourcesPromise}
			<Spinner />
		{:then impactSources}
			<div class="row g-3">
				<div class="col-6">
					<label for="resourceName">Name</label>
					<input bind:value={name} type="text" class="form-control" placeholder="Resource name" required id="resourceName" />
				</div>
				<div class="col-6">
					<label for="resourceName">Unit</label>
					<select class="form-select" bind:value={selectedImpactSource} required>
						{#each impactSources as impactSource}
							<option value={impactSource} class="form-check-input">{impactSource.name}</option>
						{/each}
					</select>
				</div>
				<div class="col-12">
					<button type="submit" data-dismiss="modal" class="btn btn-primary">Add resource</button>
				</div>
			</div>
		{:catch error}
			<Error message={error.message} />
		{/await}
	</form>
	{#if error}
		<Error message={error} />
	{/if}
</Modal>
