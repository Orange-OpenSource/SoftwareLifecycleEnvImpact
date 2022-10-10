<script lang="ts">
	import type { Model } from '$lib/model/api/model/model';
	import type { Task } from '$lib/model/api/model/task';
	import ResourceList from '$lib/model/Resource/ResourceList.svelte';
	import { changeTaskParent } from '../api/task';

	import CreateTask from './CreateTask.svelte';
	import DeleteTask from './DeleteTask.svelte';
	import RenameTask from './RenameTask.svelte';

	/* Bound vars */
	export let task: Task;
	export let selectedTask: Task;
	export let parentTask: Task;

	export let modify: boolean;
	export let selectedModel: Model;

	export let draggedObject: DragObject;

	interface DragObject {
		task: Task;
		oldParent: Task;
	}

	function handleDragStart(e) {
		e.dataTransfer.dropEffect = 'move';
		draggedObject = {
			task: task,
			oldParent: parentTask
		};
		// e.dataTransfer.setData('text', JSON.stringify(draggingObject));
	}

	async function handleDragDrop(e) {
		let oldParent = draggedObject.oldParent;
		let taskToMove = draggedObject.task;

		const res = await changeTaskParent(taskToMove, task);
		if (res) {
			console.log(res);
			// Move card to this task subtasks
			task.subtasks.push(taskToMove);
			// Remove the card to move from its old parent
			oldParent.subtasks = oldParent.subtasks.filter((t) => t.id != taskToMove.id);

			/*Redondant assignment to force Svelte to update components*/
			task.subtasks = task.subtasks;
			oldParent.subtasks = oldParent.subtasks;

			// Clear the bound object
			draggedObject = undefined;
		}
	}

	function handleDragEnd(e) {
		draggedObject = undefined;
	}
</script>

<div class={task.parent_task_id != null ? 'task' : ''}>
	<!--Do not display the root task as a nomrmal one but only its subtasks-->
	{#if task.parent_task_id != null}
		<!--Highlight border if task selected-->
		<div
			on:click|stopPropagation={() => (selectedTask = task)}
			class="card {task === selectedTask ? 'border-primary' : ''}"
			draggable="true"
			on:dragstart={handleDragStart}
			on:dragend={handleDragEnd}
			style="min-width: 18rem; width: fit-content;"
		>
			<div class="card-body">
				<div class="d-flex justify-content-between">
					<h5 class="card-title">{task.name}</h5>
					{#if modify}
						<RenameTask bind:task />
					{/if}
				</div>

				{#if task.resources.length > 0 || modify}
					<h6 class="card-subtitle mb-2 text-muted">Resources:</h6>

					<div class="card-text">
						<ResourceList bind:task {modify} />
					</div>
				{/if}
				{#if modify}
					<div class="d-flex justify-content-end">
						<DeleteTask {task} bind:parentTask />
						<CreateTask bind:parentTask={task} />
					</div>
				{/if}
			</div>
		</div>
	{/if}

	{#each task.subtasks as subtask}
		<svelte:self bind:task={subtask} bind:draggedObject bind:selectedTask bind:parentTask={task} {modify} {selectedModel} />
	{/each}

	{#if draggedObject != undefined && draggedObject.task != task}
		<div on:drop={handleDragDrop} id="drop_zone" ondragover="return false" />
	{/if}

	{#if task.parent_task_id == null && modify}
		<!--For the root task, "Add Task" button as a task in the tree-->
		<div class="task">
			<CreateTask bind:parentTask={task} />
		</div>
	{/if}
</div>

<style>
	#drop_zone {
		background-color: #eee;
		border: #999 1px solid;
		width: 280px;
		height: 200px;
		padding: 8px;
		font-size: 19px;
	}
</style>
