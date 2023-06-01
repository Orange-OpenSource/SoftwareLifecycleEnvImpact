<script lang="ts">
	import { createActivityRequest } from '$lib/api/activity';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import Modal from '$lib/Modal.svelte';
	import type { Activity } from '$lib/api/dataModel';

	/* Bound var */
	export let parentActivity: Activity;

	let showModal = false;

	let activityName: string;

	let error: string = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		activityName = '';
	}

	async function createActivity() {
		error = '';
		try {
			let res = await createActivityRequest(activityName, parentActivity.id);

			if (res) {
				parentActivity.subactivities.push(res);
				/*Redondant assignment to force Svelte to update components*/
				parentActivity.subactivities = parentActivity.subactivities;
				showModal = false;
			}
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-primary">Add subactivity</button>

<Modal bind:showModal>
	<span slot="title">Create new activity :</span>

	<form slot="body" on:submit|preventDefault={createActivity}>
		<div class="row g-3">
			<div class="col-12">
				<input placeholder="Activity name" class="form-control" bind:value={activityName} />
			</div>
			<div class="col-12">
				<button type="submit" class="btn btn-primary">Create activity</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
