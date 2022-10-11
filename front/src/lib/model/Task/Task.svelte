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

	export let draggedObject: DragObject = {};

	$: dragging = draggedObject.task != undefined;

	interface DragObject {
		task?: Task;
		oldParent?: Task;
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
		if (draggedObject.oldParent != undefined && draggedObject.task != undefined) {
			let oldParent = draggedObject.oldParent!;
			let taskToMove = draggedObject.task!;

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
				draggedObject = {};
			}
		}
	}

	function handleDragEnd(e) {
		draggedObject = {};
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
				<div class="card-title row">
					<div class="col">
						<div class="row justify-content-start">
							<div class="col-md-auto"><h5>{task.name}</h5></div>
							{#if modify && !dragging}
								<div class="col">
									<RenameTask bind:task />
								</div>
							{/if}
						</div>
					</div>

					{#if modify && !dragging}
						<div class="col-1">
							<DeleteTask {task} bind:parentTask />
						</div>
					{/if}
				</div>

				{#if !dragging}
					{#if task.resources.length > 0 || modify}
						<h6 class="card-subtitle text-muted">Resources:</h6>

						<ResourceList bind:task {modify} />
					{/if}
				{/if}
			</div>
		</div>
	{/if}

	{#each task.subtasks as subtask}
		<svelte:self bind:task={subtask} bind:draggedObject bind:selectedTask bind:parentTask={task} {modify} {selectedModel} />
	{/each}

	{#if draggedObject.task != undefined && draggedObject.task != task}
		<div on:drop={handleDragDrop} id="drop_zone" ondragover="return false" />
	{/if}

	{#if modify}
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
