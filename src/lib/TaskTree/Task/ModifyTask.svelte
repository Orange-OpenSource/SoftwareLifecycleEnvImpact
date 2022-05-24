<script lang="ts">
	import { deleteTask, updateParentTask, updateResource, updateTask } from '$lib/controllers/RequestController';
	import { createEventDispatcher } from 'svelte';
	import ModalComponent from '../../Modal.svelte';

	/* Bound var */
	export let task: any;
	export let classAttribute: string;


	let tasks = []; /*TODO logic to change parent task. Make object draggables ?*/
	let templates = [] /*TODO retrieve them*/

	const dispatch = createEventDispatcher();

	/**
	 * Delete task within the id "task.id".
	 */
	async function deleteTaskInAPI() {
		await deleteTask(task.id);
	}

	/**
	 * Update the parent of task.id to idParent.
	 */
	async function updateParent(idParent: any) {
		await updateParentTask(task.id, idParent);
	}

	/**
	 * Update task name with template.name
	 *
	 * @param template the selected template
	 */
	async function updateTaskInAPI(template: any) {
		await updateTask(task.id, template.name);
	}

	/**
	 * Update resource value with template.resource
	 *
	 * @param idResource the selected resource
	 */
	async function updateResourceInAPI(idResource: any) {
		await updateResource(idResource, document.getElementById('typeNumber' + idResource).value);

		dispatch('message', {
			text: 'updateChart'
		});
	}

	/**
	 * Set the "<select>" tag on the current parent by default.
	 *
	 * @param parentTask the parent task.
	 */
	function isParent(parentTask: { id: any }) {
		return task.parent_task_id === parentTask.id;
	}
</script>

<button on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalModifyTask{task.id}" type="button" class="btn btn-outline-primary btn-sm {classAttribute}">Modify</button>

<ModalComponent details={'ModifyTask' + task.id}>
	<!--
	<select slot="title" class="form-select">
		{#each templates as template}
			<option
				on:click={() => {
					updateTaskInAPI(template);
				}}
				selected={template.name === task.name}>{template.name}</option
			>
		{/each}
	</select>
	-->
	<button slot="btndelete" on:click={deleteTaskInAPI} type="button" class="btn btn-danger btn-sm" data-bs-dismiss="modal">Delete</button>

	<div slot="body">
		<div class="input-group mb-3">
			<label for="selectparent" class="input-group-text">Parent task</label>
			<select id="selectparent" class="form-select" style="margin: 0px;">
				{#each tasks as currentTask}
					{#if currentTask.id !== task.id}
						<option data-bs-dismiss="modal" on:click={() => updateParent(currentTask.id)} selected={isParent(currentTask)}>{currentTask.name}</option>
					{/if}
				{/each}
			</select>
		</div>

		<h2>Resources</h2>

		{#each task.resources as resource}
			<div class="input-group mb-3">
				<label class="input-group-text" for="typeNumber">{resource.name}</label>
				<input style="margin : 0px;" type="number" id="typeNumber{resource.id}" class="form-control" value={resource.value} />
				<button on:click={() => updateResourceInAPI(resource.id)} style="margin : 0px;" class="btn btn-outline-secondary" type="button">Save</button>
			</div>
		{/each}
	</div>
</ModalComponent>
