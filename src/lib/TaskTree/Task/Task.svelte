<script>
	import CreateTask from '$lib/TaskTree/Task/CreateTask.svelte';
	import ResourceList from './Resource/ResourceList.svelte';
	import DeleteTask from './DeleteTask.svelte';

	/* Bound vars */
	export let task;
	export let selectedTask;
	export let parentTask;

	export let modify;
	export let selectedModel;
	export let taskTemplates;

	function updateTaskSelected(task) {
		/*TODO maybe useless ? */
		selectedTask = task;
	}

</script>

<div class="{task.parent_task_id != null ? 'task' :''}">
	<!--Only display subtasks for the root task, not the task itself-->
	{#if task.parent_task_id != null}
		<!--Highlight border if task selected-->
		<div on:click|stopPropagation={() => updateTaskSelected(task)} class="card w-25 {task === selectedTask ? 'border-primary' : ''}" style="min-width: 18rem;">
			<div class="card-body">
				<!--
				{#if modify}
					<input type="text" value={task.name} class="form-control" style="font-size:1.2em; font-weight:bolder;">
				{:else}-->
					<h5 class="card-title">{task.name}</h5>
				<!--{/if}-->
				{#if task.resources.length > 0}
					<h6 class="card-subtitle mb-2 text-muted">Resources: </h6>

					<div class="card-text">
						<ResourceList bind:task={task} {modify}/>
					</div>
				{/if}
				{#if modify}
					<div class="d-flex justify-content-end">
						<DeleteTask bind:parentTask={parentTask} task={task}/>
						<CreateTask bind:parentTask={task} {taskTemplates} {selectedModel} />
					</div>
				{/if}
			</div>
		</div>
	{/if}

	{#each task.subtasks as subtask}
		<svelte:self bind:task={subtask} bind:selectedTask bind:parentTask={task} {modify} {selectedModel} {taskTemplates}/>
	{/each}
</div>