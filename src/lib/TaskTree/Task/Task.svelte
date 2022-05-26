<script>
	import { get } from '$lib/api';
	import CreateTask from '$lib/TaskTree/Task/CreateTask.svelte';
	import ModifyTask from '$lib/TaskTree/Task/ModifyTask.svelte';
	import { onMount } from 'svelte';

	/* Bound var */
	export let task;
	export let selectedTask;
	export let selectedModel;
	export let modify;
	export let parentTaskId;

	let taskTemplates = []

	function updateTaskSelected(task) {
		/*TODO maybe useless ? */
		selectedTask = task;
	}

	function isLeaf(task){
		return task.subtasks.length === 0
	}

	onMount(async function () {
		taskTemplates = await get('tasktemplates')
	});
</script>

<div class="tree">
	{#if isLeaf(task)}
		{#if modify}
			<div class="raw nochildmodify">
				<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
					{task.name}
					<ModifyTask {taskTemplates} bind:task={task} classAttribute={'btnmodify'} />
				</span>
				<span class="addtask">
					<CreateTask {taskTemplates} {selectedModel} parent_task_id={parentTaskId} />
				</span>
			</div>
		{:else}
			<div class="raw">
				<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
					{task.name}
				</span>
			</div>
			{/if}
	{:else}
		<div class="raw">
			<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
				{task.name}
				{#if modify}
					<ModifyTask {taskTemplates} bind:task={task} classAttribute={'btnmodifyparent'} />
				{/if}
			</span>
			{#each task.subtasks as subtask}
				<svelte:self bind:task={subtask} bind:selectedTask {modify} {selectedModel} parentTaskId={task.id}/>
			{/each}
			<div class="tree">
				<CreateTask {taskTemplates} {selectedModel} parent_task_id={parentTaskId} />
			</div>
		</div> 
	{/if}
</div>