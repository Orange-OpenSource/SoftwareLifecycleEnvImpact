<script>
	import CreateTask from '$lib/TaskTree/Task/CreateTask.svelte';
	import ResourceList from './Resource/ResourceList.svelte';
	import DeleteTask from './DeleteTask.svelte';

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
</script>

<div class="{task.parent_task_id != null ? 'task' :''}">
	<!--Only display subtasks for the root task, not the task itself-->
	{#if task.parent_task_id != null}
		<div on:click|stopPropagation={() => updateTaskSelected(task)} class="card btn-task-tile w-50">
			<div class="card-body">
				<div class="row">
					{#if modify}
						<input type="text" value={task.name} class="form-control" style="font-size:1.2em; font-weight:bolder;">
					{:else}
						<h3 class="card-title">{task.name}</h3>
					{/if}
				</div>

				<ResourceList resources={task.resources} {modify}/>

				{#if modify}
					<div class="row">
						<DeleteTask bind:task={task}/>
						<CreateTask bind:parentTask={task} {taskTemplates} {selectedModel} />
					</div>
				{/if}
			</div>
		</div>
	{/if}

	{#each task.subtasks as subtask}
		<svelte:self bind:task={subtask} bind:selectedTask {modify} {selectedModel} parentTask={task} {taskTemplates}/>
	{/each}
</div>