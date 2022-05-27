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
	export let parentTask;
	export let taskTemplates;

	function updateTaskSelected(task) {
		/*TODO maybe useless ? */
		selectedTask = task;
	}

	function isLeaf(task){
		return task.subtasks.length === 0
	}
</script>

<!--Only display subtasks for the root task, not the task itself-->
{#if task.parent_task_id != null}
	<div class="tree">
		{#if isLeaf(task)}
			{#if modify}
				<div class="nochildmodify">
					<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
						{task.name}
						<ModifyTask {taskTemplates} bind:task={task} classAttribute={'btnmodify'} />
					</span>
					<span class="addtask">
						<CreateTask  bind:parentTask={task} {taskTemplates} {selectedModel}/>
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
					<svelte:self bind:task={subtask} bind:selectedTask {modify} {selectedModel} parentTask={task} {taskTemplates}/>
				{/each}
				{#if modify}
					<div class="tree">
						<CreateTask bind:parentTask={task} {taskTemplates} {selectedModel} />
					</div>
				{/if}
			</div> 
		{/if}
	</div>
{:else}
	{#each task.subtasks as subtask}
		<svelte:self bind:task={subtask} bind:selectedTask {selectedModel} {modify} parentTask={task} {taskTemplates}/>
	{/each}
	{#if modify}
		<div class="tree">
			<CreateTask bind:parentTask={parentTask} {taskTemplates} {selectedModel}  />
		</div>
	{/if}
{/if}

