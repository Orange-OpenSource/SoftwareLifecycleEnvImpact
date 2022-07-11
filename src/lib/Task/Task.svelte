<script>
	import ResourceList from '../Resource/ResourceList.svelte';
	import CreateTask from './CreateTask.svelte';
	import DeleteTask from './DeleteTask.svelte';
	import RenameTask from './RenameTask.svelte';

	/* Bound vars */
	export let task;
	export let selectedTask;
	export let parentTask;

	export let modify;
	export let selectedModel;
	export let taskTemplates;
</script>

<div class="{task.parent_task_id != null ? 'task' :''}">
	<!--Do not display the root task as a nomrmal one but only its subtasks-->
	{#if task.parent_task_id != null}
		<!--Highlight border if task selected-->
		<div on:click|stopPropagation={() => selectedTask = task} class="card {task === selectedTask ? 'border-primary' : ''}" style="min-width: 18rem;">
			<div class="card-body">
				<div class="d-flex">
					<h5 class="card-title">{task.name}</h5>
					{#if modify}
						<RenameTask bind:task/>
					{/if}
				</div>

				{#if task.resources.length > 0}
					<h6 class="card-subtitle mb-2 text-muted">Resources: </h6>

					<div class="card-text">
						<ResourceList bind:task {modify}/>
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

	{#if task.parent_task_id == null && modify}
		<!--For the root task, "Add Task" button as a task in the tree-->
		<div class='task'>
			<CreateTask bind:parentTask={task} {taskTemplates} {selectedModel} />
		</div>
	{/if}

</div>