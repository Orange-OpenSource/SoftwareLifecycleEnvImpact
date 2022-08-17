<script lang="ts">
	import { del } from '$lib/api/api';
import { deleteResourceRequest } from '$lib/api/resource';
	import Modal from '$lib/Modal.svelte';
	import type { Resource } from 'src/model/resource';
	import type { Task } from 'src/model/task';

	/*Bound var*/
	export let task: Task;

	export let resource: Resource;

	let showModal = false;
	let error = '';

	async function deleteResource() {
		await deleteResourceRequest(resource);
		task.resources = task.resources.filter(r => r.id != resource.id);
		showModal = false;
	}
</script>

<input on:click|stopPropagation={() => (showModal = true)} type="image" src="/trash.svg" width="25" height="25" alt="Bin" loading="lazy" />

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{resource.name}</strong> ?</span>

	{#if error != ''}
		<p style="color: red">{error}</p>
	{/if}

	<button on:click|stopPropagation={() => deleteResource()} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
