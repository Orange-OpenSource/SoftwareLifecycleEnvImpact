<script>
	import { del, patch } from '$lib/api';
	import ModalComponent from '../../Modal.svelte';

	/* Bound var */
	export let task;
	export let classAttribute;
	export let taskTemplates;

	async function deleteTask() {
		const res = await del('tasks/'+task.id)

		if (res.status === 404) alert('No task with this id');
		else if (res.status === 403) alert('Cannot delete the root task of a model');
	}

	async function updateTask(template) {
		const res = await patch('tasks/'+task.id, [
			{
				op: 'replace',
				path: '/name',
				value: template.name
			}
		])

		if (res.status === 403) alert('Patch format is incorrect');
		else if (res.status === 404) alert('No task found with this id')
		else {
			task.name = res.name
		}
	}

	async function updateResource(resource){
		const newValue = document.getElementById('typeNumber' + resource.id).value
		const res = await patch('resource/' + resource.id,[
			{
				op: 'replace',
				path: '/value',
				value: newValue
			}
		])

		if (res.status === 403) alert('Patch format is incorrect');
		else if (res.status === 404) alert('No resource found with this id' + resource.id);
		else{
			resource.value = res.value
		}

	}
</script>

<button on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalModifyTask{task.id}" type="button" class="btn btn-outline-primary btn-sm {classAttribute}">Modify</button>

{#if taskTemplates != null}
	<ModalComponent details={'ModifyTask' + task.id}>
		<select slot="title" class="form-select">
			{#each taskTemplates as template}
				<option
					on:click={() => {
						updateTask(template);
					}}
					selected={template.name === task.name}>{template.name}</option
				>
			{/each}
		</select>
		<button slot="btndelete" on:click={deleteTask} type="button" class="btn btn-danger btn-sm" data-bs-dismiss="modal">Delete</button>

		<div slot="body">
			<h2>Resources</h2>

			{#each task.resources as resource}
				<div class="input-group mb-3">
					<label class="input-group-text" for="typeNumber">{resource.name}</label>
					<input style="margin : 0px;" type="number" id="typeNumber{resource.id}" class="form-control" value={resource.value} />
					<button on:click={() => updateResource(resource)} style="margin : 0px;" class="btn btn-outline-secondary" type="button">Save</button>
				</div> TODO FROM HERE PASSER EN FORME POUR QUE L4IMAPCT SUPDATE APRES MODIFICATION RESOURCE
			{/each}
		</div>
	</ModalComponent>
{/if}

