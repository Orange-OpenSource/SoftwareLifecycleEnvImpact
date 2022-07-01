<script>
	import { del, patch } from '$lib/api';
	import Modal from '../Modal.svelte'

	/* Bound var */
	export let task;

	let showModal = false;

	let newName = task.name
	let error = '';
	
	async function renameTask(template) {
		const res = await patch('tasks/'+task.id, [
			{
				op: 'replace',
				path: '/name',
				value: newName
			}
		])

		error = '' 
		switch (res.status) {
            case undefined:
			task.name = res.name
			showModal = false
				break;
			case 403:
				error = 'Patch format is incorrect'
				break;
            case 404:
                error = 'No task found with this id'
				break;
            default:
                error = res.status + ' error'
				break;
        }
	}
</script>

<button on:click|stopPropagation={() => showModal = true} class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename task</span>
	<form slot="body" on:submit|preventDefault={renameTask}>
		<input id="renameTask" placeholder="Task name" required bind:value={newName}/>
		{#if error != ''}
			<p style="color: red">{error}</p>
		{/if}
		<button type="submit" class="btn btn-primary">Rename task</button>
	</form>
</Modal>