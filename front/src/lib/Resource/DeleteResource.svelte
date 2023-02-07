<script lang="ts">
	import { deleteResourceRequest } from '$lib/api/resource';
	import Modal from '$lib/Modal.svelte';
	import Error from '$lib/Error.svelte';
	import type { Resource, Task } from '$lib/api/dataModel';
	import Icon from '@iconify/svelte';

	/*Bound var*/
	export let task: Task;

	export let resource: Resource;

	let showModal = false;
	let error = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

	async function deleteResource() {
		error = '';
		try {
			await deleteResourceRequest(resource);
			task.resources = task.resources.filter((r) => r.id != resource.id);
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

	<form slot="body" on:submit|preventDefault={deleteResource}>
		<div class="row g-3">
			<div class="col-12">
				<p>Are you sure you want to delete resource <strong>{resource.name}</strong> ?</p>
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
