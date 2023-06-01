<script lang="ts">
	import Modal from '$lib/Modal.svelte';
	import { getImpactSources } from '$lib/api/impactSources';
	import { addResourceRequest } from '$lib/api/resource';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import type { ImpactSource, Activity } from '$lib/api/dataModel';

	/*Bound var*/
	export let activity: Activity;

	let showModal = false;

	let impactSourcesPromise = getImpactSources();
	let selectedImpactSource: ImpactSource;

	let error = '';
	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

	async function handleSubmit() {
		// TODO error marche pas à cause du async
		error = '';
		try {
			if (selectedImpactSource != null) {
				const res = await addResourceRequest(activity.id, selectedImpactSource);
				activity.resources.push(res);
				/*Redondant assignment to force Svelte to update components*/
				activity.resources = activity.resources;
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
