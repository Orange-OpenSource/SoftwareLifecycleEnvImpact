<script lang="ts">
	import { deleteResourceRequest } from '$lib/api/resource';
	import Modal from '$lib/Modal.svelte';
	import type { Resource } from 'src/model/resource';
	import type { Task } from 'src/model/task';
	import Error from '$lib/Error.svelte';

	/*Bound var*/
	export let task: Task;

	export let resource: Resource;

	let showModal = false;
	let error = '';

	$: showModal, error = '' //Clean error message when closing modal

	async function deleteResource() {
		error = ''
		try{
			await deleteResourceRequest(resource);
			task.resources = task.resources.filter((r) => r.id != resource.id);
			showModal = false;
		}catch(e: any){
			error = e.message
		} 
	}
</script>

<input on:click|stopPropagation={() => (showModal = true)} type="image" src="/trash.svg" width="25" height="25" alt="Bin" loading="lazy" />

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{resource.name}</strong> ?</span>

	{#if error}
		<Error message={error} />
	{/if}

	<button on:click|stopPropagation={() => deleteResource()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
