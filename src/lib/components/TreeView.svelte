<script lang="ts">
	import ModalComponent from './ModalComponent.svelte';

	export let subtasks: any;
	export let modify: any;
</script>

{#each subtasks as task}
	<div class="tree">
		{#if task.subtasks}
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

						<ModalComponent task_id={task.id}>
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

				<svelte:self subtasks={task.subtasks} {modify} />
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

					<ModalComponent task_id={task.id}>
						<span slot="taskName">{task.name}</span>
						<span slot="body"> To do </span>
					</ModalComponent>
				</span>
				<span class="addtask"><button class="btn btn-primary">Add task</button></span>
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
	<div class="tree"><button class="btn btn-primary">Add task</button></div>
{/if}
