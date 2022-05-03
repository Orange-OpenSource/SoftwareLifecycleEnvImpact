<script lang="ts">
	import { deleteTask } from '$lib/controllers/RequestController';
	import { createEventDispatcher } from 'svelte';

	export let task_id: any;
	export let task_parent_id: any;
	export let tasks: any[];

	const dispatch = createEventDispatcher();

	async function deleteTaskInAPI() {
		await deleteTask(task_id);

		dispatch('message', {
			text: 'updateTree'
		});
	}

	async function updateParent(idParent: any){
		console.log(idParent);
	}

	function isParent(task: { parent_task_id: any; }, parentTask: { id: any; }){
		return task_parent_id === parentTask.id;
	}
</script>

<div
	class="modal fade"
	id="modal{task_id}"
	tabindex="-1"
	aria-labelledby="modalLabel{task_id}"
	aria-hidden="true"
>
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<div class="w-100 d-flex justify-content-between">
					<h5 class="modal-title" id="modalLabel{task_id}"><slot name="taskName" /></h5>
					<button
						on:click={deleteTaskInAPI}
						type="button"
						class="btn btn-danger btn-sm"
						data-bs-dismiss="modal">Delete</button
					>
				</div>
				<button
					type="button"
					class="btn-close"
					style="margin-left:10px;"
					data-bs-dismiss="modal"
					aria-label="Close"
				/>
			</div>
			<div class="modal-body">
				Parent :
				<select class="form-select" aria-label="Default select example">
					{#each tasks as task}
						{#if task.id !== task_id}
						<option on:click={() => updateParent(task.id)}
							selected={isParent(task_id, task)}
							>{task.name}</option
						>
						{/if}
					{/each}
				</select>

				<slot name="body" />
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
			</div>
		</div>
	</div>
</div>
