<script>
	import { del, patch } from '$lib/api';
	import ModalComponent from '../../Modal.svelte';
	import ResourceList from './Resource/ResourceList.svelte';

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
</script>

<button on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalModifyTask{task.id}" type="button" class="btn btn-primary btn-sm">Modify</button>

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
			<ResourceList resources={task.resources}/>
		</div>
	</ModalComponent>
{/if}

