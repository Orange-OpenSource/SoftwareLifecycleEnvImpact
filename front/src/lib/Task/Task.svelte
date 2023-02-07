<script lang="ts">
	import type { Model, Task } from '$lib/api/dataModel';
	import { changeTaskParent } from '$lib/api/task';
	import ResourceList from '$lib/Resource/ResourceList.svelte';

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

	let draggingOver = false;

	$: dragging = draggedObject.task != undefined;

	$: task, updateImpact();

	function updateImpact() {
		// Little hack to trigger a re-draw of impacts by updating
		// the selectedTask even if another one is modified
		selectedTask = selectedTask;
	}

	interface DragObject {
		task?: Task;
		oldParent?: Task;
	}

	function handleDragOver(e) {
		draggingOver = true;
	}

	function handleDragLeave(e) {
		draggingOver = false;
	}

	function handleMouseDown(e) {
		// The the task as draggable only when cliking on the header
		e.target.parentNode.setAttribute('draggable', 'true');
	}

	function handleMouseUp(e) {
		// When click on header over, task is not draggable anymore
		e.target.parentNode.setAttribute('draggable', 'false');
	}

	function handleDragStart(e: any) {
		e.dataTransfer.dropEffect = 'move';
		draggedObject = {
			task: task,
			oldParent: parentTask
		};
		// e.dataTransfer.setData('text', JSON.stringify(draggingObject));
	}

	async function handleDragDrop(e: any) {
		if (draggedObject.oldParent != undefined && draggedObject.task != undefined) {
			let oldParent = draggedObject.oldParent!;
			let taskToMove = draggedObject.task!;

			const res = await changeTaskParent(taskToMove, task);
			if (res) {
				taskToMove.subtasks.forEach((_, index) => {
					taskToMove.subtasks[index].parent_task_id = oldParent.id;
				});
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

	function handleDragEnd(e: any) {
		draggedObject = {};
		e.target.setAttribute('draggable', 'false'); //Task not draggable anymore
	}
</script>

<div class={task.parent_task_id != null ? 'task' : ''}>
	<!--Do not display the root task as a nomrmal one but only its subtasks-->
	{#if task.parent_task_id != null}
		<!--Highlight border if task selected-->
		<div
			on:click|stopPropagation={() => (selectedTask = task)}
			class="card {selectedTask.id == task.id ? 'border-primary' : ''}"
			on:dragstart={handleDragStart}
			on:dragend={handleDragEnd}
			style="width: fit-content;"
		>
			<div id="mydivheader" class="card-header" hidden={!modify || dragging}>
				<div class="d-flex justify-content-between">
					<div class="col-8" style="cursor: move;" on:mousedown={handleMouseDown} on:mouseup={handleMouseUp}>Click here to drag</div>
					<div class="col-2"><DeleteTask {task} bind:parentTask bind:selectedTask /></div>
				</div>
			</div>
			<div class="card-body">
				<div class="card-title">
					<div class="d-flex flex-row">
						<div class="p-0"><h5>{task.name}</h5></div>
						{#if modify && !dragging}
							<div class="p-0">
								<RenameTask bind:task />
							</div>
						{/if}
					</div>
				</div>

				{#if !dragging}
					{#if task.resources.length > 0 || modify}
						<ResourceList bind:task {modify} />
					{/if}
				{/if}
			</div>
		</div>
	{/if}

	{#each task.subtasks as subtask}
		<svelte:self bind:task={subtask} bind:draggedObject bind:selectedTask bind:parentTask={task} {modify} {selectedModel} />
	{/each}

	{#if draggedObject.task != undefined && draggedObject.task != task && draggedObject.task.parent_task_id != task.id}
		<div class="task" on:drop={handleDragDrop} on:dragover={handleDragOver} on:dragleave={handleDragLeave}>
			<div class="col-8 card {draggingOver ? 'border-success' : ''}" style="min-width: 15rem;">
				<div class="card-body ">
					<small>Drop here</small>
				</div>
			</div>
		</div>
	{:else if modify}
		<!--"Add Task" button as a task in the tree-->
		<div class="task">
			<CreateTask bind:parentTask={task} />
		</div>
	{/if}
</div>
