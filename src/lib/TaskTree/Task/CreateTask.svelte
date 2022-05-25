<script>
	import ModalComponent from '../../Modal.svelte';
	import { post } from '$lib/api';

	/* Bound var */
	export let selectedModel;
	export let parent_task_id;
	export let taskTemplates;

	/**
	 * Create a new task with the given parent.
	 *
	 * @param parentId The parent id of the new task.
	 */
	async function createNewTask(parentId) {
		let input = document.getElementById('createTaskInput' + parentId);

		let template_id = input.value;
		let template_name = input.options[input.selectedIndex].text;

		console.log(template_id)
		console.log(parseInt(template_id))

		const res = await post('tasks', {
			model_id: selectedModel.id,
			name: template_name,
			parent_task_id: parentId,
			template_id: parseInt(template_id)
		})

		if (res.status === 409) alert('Task already exists on this level');
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateTask{parent_task_id}" class="btn btn-primary">Add task</button>

<ModalComponent details={'CreateTask' + parent_task_id}>
	<span slot="title">Create new task :</span>
	<div slot="body">
		<select id="createTaskInput{parent_task_id}" class="form-select">
			<option disabled selected value> -- Templates -- </option>
			{#each taskTemplates as template}
				<option on:click={() => {}} value={template.id}>{template.name}</option>
			{/each}
		</select>
	</div>
	<button on:click={() => createNewTask(parent_task_id)} data-bs-dismiss="modal" slot="btnsave" type="button" class="btn btn-primary">Create task</button>
</ModalComponent>
