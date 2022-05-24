<script lang="ts">
	import ModalComponent from '../../Modal.svelte';
	import { createTask } from '$lib/controllers/RequestController';

	/* Bound var */
	export let selectedModel;
	export let parent_task_id: any;


	export let templates = []


	/**
	 * Create a new task with the given parent.
	 *
	 * @param parentId The parent id of the new task.
	 */
	async function createNewTask(parentId: any) {
		let input = document.getElementById('createTaskInput' + parentId);

		let template_id = input.value;
		let template_name = input.options[input.selectedIndex].text;

		let newTask = await createTask(selectedModel, template_name, parentId, template_id);

		if (newTask.status === 409) alert('Task already exists on this level');

	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateTask{parent_task_id}" class="btn btn-primary">Add task</button>

<ModalComponent details={'CreateTask' + parent_task_id}>
	<span slot="title">Create new task :</span>
	<div slot="body">
		<select id="createTaskInput{parent_task_id}" class="form-select">
			{#each templates as template}
				<option on:click={() => {}} value={template.id}>{template.name}</option>
			{/each}
		</select>
	</div>
	<button on:click={() => createNewTask(parent_task_id)} data-bs-dismiss="modal" slot="btnsave" type="button" class="btn btn-primary">Create task</button>
</ModalComponent>
