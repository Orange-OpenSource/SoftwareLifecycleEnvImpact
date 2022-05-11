<script lang="ts">
	import ModalModifyTask from './modals/ModalModifyTask.svelte';
	import { onMount } from 'svelte';

	export let subtasks: any;
	export let modify: any;
	export let model_id: any;
	export let parent_task_id: any;
	export let tasks: any[];
	export let templates: any;

	let ModalCreationTask: any;

	onMount(async function () {
		const module = await import('./modals/ModalCreationTask.svelte');
		ModalCreationTask = module.default;
	});
</script>

{#each subtasks as task}
	<div class="tree">
		{#if task.subtasks.length !== 0}
			<div class="raw">
				<span class="info-name">
					{task.name}
					{#if modify}
						<ModalModifyTask on:message bind:tasks bind:templates {task} classAttribute={'btnmodifyparent'} />
					{/if}
				</span>

				<svelte:self on:message subtasks={task.subtasks} bind:modify parent_task_id={task.id} {model_id} {tasks} />
			</div>
		{:else if modify}
			<div class="raw nochildmodify">
				<span class="info-name">
					{task.name}
					<ModalModifyTask on:message bind:tasks bind:templates {task} classAttribute={'btnmodify'} />
				</span>
				<span class="addtask">
					<svelte:component this={ModalCreationTask} on:message bind:model_id bind:task_id={task.id} />
				</span>
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
		<svelte:component this={ModalCreationTask} on:message bind:model_id bind:task_id={parent_task_id} />
	</div>
{/if}
