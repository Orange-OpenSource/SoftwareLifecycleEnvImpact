<script lang="ts">
	import Error from '$lib/Error.svelte';
	import { renameActivityRequest } from '$lib/api/activity';
	import Modal from '$lib/Modal.svelte';
	import type { Activity } from '$lib/api/dataModel';
	import Icon from '@iconify/svelte';

	/* Bound var */
	export let activity: Activity;

	let showModal = false;
	let error = '';
	let newName = activity.name;

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		newName = activity.name;
	}

	async function renameActivity() {
		error = '';
		try {
			const res = await renameActivityRequest(activity, newName);
			activity.name = res.name;
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button class="btn btn-sm" on:click|stopPropagation={() => (showModal = true)}>
	<Icon icon="material-symbols:edit-outline" width="25" height="25" alt="Duplicate" loading="lazy" />
</button>
<Modal bind:showModal>
	<span slot="title">Rename activity</span>

	<form slot="body" on:submit|preventDefault={renameActivity}>
		<div class="row g-3">
			<div class="col-12">
				<!-- TODO label ? -->
				<input class="form-control" placeholder="Activity new name" required bind:value={newName} />
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-primary">Rename activity</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
