<script lang="ts">
	import ModalComponent from './ModalComponent.svelte';
	import ModalCreationTaskComponent from './ModalCreationTaskComponent.svelte';
	import { createEventDispatcher } from 'svelte';
	import { createTask } from '$lib/controllers/RequestController';

	const dispatch = createEventDispatcher();
	export let subtasks: any;
	export let modify: any;
	export let model_id: any;
	export let parent_task_id: any;
	export let tasks: any[];

	async function createNewTask(parentId: any) {
		// @ts-ignore
		let taskname = document.getElementById('createTaskInput' + parentId).value;

		await createTask(model_id, taskname, parentId, 0);

		dispatch('message', {
			text: 'updateTree'
		});
	}
</script>

{#each subtasks as task}
	<div class="tree">
		{#if task.subtasks.length !== 0}
			<div class="raw">
				<span class="info-name">
					{task.name}
					{#if modify}
						<button
							data-bs-toggle="modal"
							data-bs-target="#modal{task.id}"
							type="button"
							class="btn btn-outline-primary btn-sm btnmodifyparent">Modify</button
						>

						<ModalComponent on:message bind:tasks={tasks} task_id={task.id} task_parent_id={task.parent_task_id}>
							<span slot="taskName">{task.name}</span>
							<span id="task_id{task.id}" slot="body">
								{#each task.inputs as input}
									<label for="taskinput">{input.name}</label>
									{#if input.kind == 'string'}
										<input
											class="input-group"
											type="text"
											id="taskinput"
											name="taskinput{input.id}"
											required
										/>
									{:else if input.kind == 'float'}
										<input
											class="input-group"
											type="number"
											id="taskinput"
											name="taskinput{input.id}"
											required
										/>
									{:else}
										Not implemented
									{/if}
								{/each}
							</span>
						</ModalComponent>
					{/if}
				</span>

				<svelte:self
					on:message
					subtasks={task.subtasks}
					{modify}
					parent_task_id={task.id}
					{model_id}
					{tasks}
				/>
			</div>
		{:else if modify}
			<div class="raw nochildmodify">
				<span class="info-name">
					{task.name}
					<button
						data-bs-toggle="modal"
						data-bs-target="#modal{task.id}"
						type="button"
						class="btn btn-outline-primary btn-sm btnmodify">Modify</button
					>

					<ModalComponent bind:tasks={tasks} on:message task_id={task.id} task_parent_id={task.parent_task_id}>
						<span slot="taskName">{task.name}</span>
						<span id="task_id{task.id}" slot="body">
							{#each task.inputs as input}
								<label for="taskinput">{input.name}</label>
								{#if input.kind == 'string'}
									<input
										class="input-group"
										type="text"
										id="taskinput"
										name="taskinput{input.id}"
										required
									/>
								{:else if input.kind == 'float'}
									<input
										class="input-group"
										type="number"
										id="taskinput"
										name="taskinput{input.id}"
										required
									/>
								{:else}
									Not implemented
								{/if}
							{/each}
						</span>
					</ModalComponent>
				</span>
				<span class="addtask"
					><button
						data-bs-toggle="modal"
						data-bs-target="#modalCreateTask{task.id}"
						class="btn btn-primary">Add task</button
					></span
				>

				<ModalCreationTaskComponent task_id={task.id}>
					<span slot="taskName">Create new task :</span>
					<input slot="body" id="createTaskInput{task.id}" placeholder="Task name" required />
					<button
						on:click={() => createNewTask(task.id)}
						slot="btnsave"
						type="button"
						data-bs-dismiss="modal"
						class="btn btn-primary">Create task</button
					>
				</ModalCreationTaskComponent>
			</div>
		{:else}
			<div class="raw nochild">
				<span class="info-name">
					{task.name}
				</span>
			</div>
		{/if}
	</div>
{/each}
{#if modify}
	<div class="tree">
		<button
			data-bs-toggle="modal"
			data-bs-target="#modalCreateTask{parent_task_id}"
			class="btn btn-primary">Add task</button
		>
		<ModalCreationTaskComponent task_id={parent_task_id}>
			<span slot="taskName">Create new task :</span>
			<input slot="body" id="createTaskInput{parent_task_id}" placeholder="Task name" required />
			<button
				on:click={() => createNewTask(parent_task_id)}
				slot="btnsave"
				type="button"
				data-bs-dismiss="modal"
				class="btn btn-primary">Create task</button
			>
		</ModalCreationTaskComponent>
	</div>
{/if}
