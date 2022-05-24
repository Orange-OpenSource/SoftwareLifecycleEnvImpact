<script lang="ts">
	import ModalCreationTask from '$lib/components/modals/ModalCreationTask.svelte';
	import { getModelImpact } from '$lib/controllers/RequestController';
	import ModalModifyTask from '../components/modals/ModalModifyTask.svelte';

	/* Bound var */
	export let selectedTask
	export let selectedModel,
	export let subtasks: any;
	export let modify: any;
	export let parent_task_id: any;
	export let tasks: any[];


    function updateTaskSelected(task) { /*TODO maybe useless ? */
		console.log(task)
		selectedTask = task
	}
	
</script>

{#each subtasks as task}
	<div class="tree">
		{#if task.subtasks.length !== 0}
			<div class="raw">
				<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
					{task.name}
					{#if modify}
						<ModalModifyTask bind:task classAttribute={'btnmodifyparent'}/>
					{/if}
				</span>
				<svelte:self on:message subtasks={task.subtasks} bind:modify parent_task_id={task.id} {selectedModel} {tasks} />
			</div>
		{:else if modify}
			<div class="raw nochildmodify">
				<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
					{task.name}
					<ModalModifyTask on:message bind:task classAttribute={'btnmodify'} />
				</span>
				<span class="addtask">
					<ModalCreationTask on:message bind:selectedModel bind:task_id={task.id} />
				</span>
			</div>
		{:else}
			<div class="raw nochild">
				<span on:click|stopPropagation={() => updateTaskSelected(task)} class="info-name">
					{task.name}
				</span>
			</div>
		{/if}
	</div>
{/each}
{#if modify}
	<div class="tree">
		<ModalCreationTask on:message {selectedModel} {parent_task_id} />
	</div>
{/if}
