<script>
	import ModalComponent from '../../Modal.svelte';
	import { post } from '$lib/api';

	/* Bound var */
	export let parentTask;

	export let selectedModel;
	export let taskTemplates;

	let selectedTemplate;

	async function handleSubmit(){
		if(selectedTemplate != null){
			const res = await post('tasks', {
				model_id: selectedModel.id,
				name: selectedTemplate.name,
				parent_task_id: parentTask.id,
				template_id: selectedTemplate.id
			})

			if (res.status === 409) alert('Task already exists on this level');
			else{
				parentTask.subtasks.push(res)
				/*Redondant assignment to force Svelte to update components*/
				parentTask.subtasks = parentTask.subtasks
			}
		}
	}
</script>

<button data-bs-toggle="modal" data-bs-target="#modalCreateTask{parentTask.id}" class="btn btn-primary">Add task</button>

{#if taskTemplates != undefined}
	<ModalComponent details={'CreateTask' + parentTask.id}>
		<span slot="title">Create new task :</span>
		<form slot="body" on:submit|preventDefault={handleSubmit}>
			<select id="templateSelect" class="form-select" bind:value={selectedTemplate}>
				<option value={null} disabled selected class="form-check-input"> -- Templates -- </option>
				{#each taskTemplates as template}
					<option value={template}>{template.name}</option>
				{/each}
			</select>
			<button data-bs-dismiss="modal" type="submit" class="btn btn-primary">Create task</button>
		</form>
	</ModalComponent>
{/if}
