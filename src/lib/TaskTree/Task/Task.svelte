<script>
import { get } from '$lib/api';

	import CreateTask from '$lib/TaskTree/Task/CreateTask.svelte';
	import ModifyTask from '$lib/TaskTree/Task/ModifyTask.svelte';
import { onMount } from 'svelte';

	/* Bound var */
	export let selectedTask;
	export let selectedModel;
	export let subtasks;
	export let modify;
	export let parent_task_id;
	export let tasks;

	let taskTemplates = []

	function updateTaskSelected(task) {
		/*TODO maybe useless ? */
		selectedTask = task;
	}

	onMount(async function () {
		taskTemplates = await get('tasktemplates')
	});
</script>

{#each subtasks as task}
	<div class="tree">
		{#if task.subtasks.length !== 0}
			<div class="raw">
				<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
					{task.name}
					{#if modify}
						<ModifyTask {taskTemplates} bind:task classAttribute={'btnmodifyparent'} />
					{/if}
				</span>
				<svelte:self subtasks={task.subtasks} bind:modify parent_task_id={task.id} {selectedModel} {tasks} />
			</div>
		{:else if modify}
			<div class="raw nochildmodify">
				<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
					{task.name}
					<ModifyTask {taskTemplates} bind:task classAttribute={'btnmodify'} />
				</span>
				<span class="addtask">
					<CreateTask {taskTemplates} bind:selectedModel bind:task_id={task.id} />
				</span>
			</div>
		{:else}
			<div class="raw nochild">
				<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
					{task.name}
				</span>
			</div>
		{/if}
	</div>
{/each}
{#if modify}
	<div class="tree">
		<CreateTask {taskTemplates} {selectedModel} {parent_task_id} />
	</div>
{/if}
