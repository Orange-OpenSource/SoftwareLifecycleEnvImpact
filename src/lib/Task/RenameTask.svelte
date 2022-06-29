<script>
	import { del, patch } from '$lib/api';
	import Modal from '../Modal.svelte'

	/* Bound var */
	export let task;

	let showModal = false;

	let newName = task.name
	
	async function renameTask(template) {
		const res = await patch('tasks/'+task.id, [
			{
				op: 'replace',
				path: '/name',
				value: newName
			}
		])
		if (res.status === 403) alert('Patch format is incorrect');
		else if (res.status === 404) alert('No task found with this id')
		else {
			task.name = res.name
			showModal = false
		}
	}
</script>

<button on:click|stopPropagation={() => showModal = true} class="btn btn-light">Rename</button>

<Modal bind:showModal>
	<span slot="title">Rename task</span>
	<form slot="body" on:submit|preventDefault={renameTask}>
		<input id="renameTask" placeholder="Task name" required bind:value={newName}/>
		<button type="submit" class="btn btn-primary">Rename task</button>
	</form>
</Modal>