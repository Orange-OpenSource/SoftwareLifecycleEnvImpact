<script lang="ts">
	import { deleteActivityRequest } from '$lib/api/activity';
	import Modal from '$lib/Modal.svelte';
	import Error from '$lib/Error.svelte';
	import type { Activity } from '$lib/api/dataModel';
	import Icon from '@iconify/svelte';

	/* Bound var */
	export let parentActivity: Activity;
	export let selectedActivity: Activity;

	export let activity: Activity;

	let showModal = false;

	let error = '';
	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

	async function deleteActivity() {
		error = '';
		try {
			await deleteActivityRequest(activity);
			parentActivity.subactivities = parentActivity.subactivities.filter((s) => s.id != activity.id);
			/*Redondant assignment to force Svelte to update components*/
			parentActivity.subactivities = parentActivity.subactivities;
			if (activity.id == selectedActivity.id) {
				selectedActivity = parentActivity;
			}
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button class="btn" on:click|stopPropagation={() => (showModal = true)}>
	<Icon icon="ion:trash-outline" width="25" height="25" alt="Delete" loading="lazy" />
</button>
<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<form slot="body" on:submit|preventDefault={deleteActivity}>
		<div class="row g-3">
			<div class="col-12">
				<p>Are you sure you want to delete activity <strong>{activity.name}</strong> ?</p>
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-danger">Delete</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
