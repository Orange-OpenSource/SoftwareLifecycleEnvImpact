<script lang="ts">
	import { onMount } from 'svelte';

	export let subtasks: any;
	export let modify: any;
	export let model_id: any;
	export let parent_task_id: any;
	export let tasks: any[];
	export let templates: any;
	export let myChart: any;

	let ModalCreationTask: any;
	let ModalModifyTask: any;

	/**
	 * Update the chart with the new data.
	 */
	function updateChart(task_id: any) {
		// todo : routes impact
		//myChart.data.labels = labels;
		//myChart.data.datasets[0].data = data;
		myChart.update();
		console.log('update ' + task_id);
	}

	onMount(async function () {
		const module = await import('./modals/ModalCreationTask.svelte');
		ModalCreationTask = module.default;

		const modulemodify = await import('./modals/ModalModifyTask.svelte');
		ModalModifyTask = modulemodify.default;
	});
</script>

{#each subtasks as task}
	<div class="tree">
		{#if task.subtasks.length !== 0}
			<div class="raw">
				<span on:click|stopPropagation={() => updateChart(task.id)} class="info-name">
					{task.name}
					{#if modify}
						<svelte:component this={ModalModifyTask} on:message bind:tasks bind:templates {task} classAttribute={'btnmodifyparent'} />
					{/if}
				</span>

				<svelte:self on:message subtasks={task.subtasks} bind:templates bind:myChart bind:modify parent_task_id={task.id} {model_id} {tasks} />
			</div>
		{:else if modify}
			<div class="raw nochildmodify">
				<span on:click|stopPropagation={() => updateChart(task.id)} class="info-name">
					{task.name}
					<svelte:component this={ModalModifyTask} on:message bind:tasks bind:templates {task} classAttribute={'btnmodify'} />
				</span>
				<span class="addtask">
					<svelte:component this={ModalCreationTask} on:message bind:templates bind:model_id bind:task_id={task.id} />
				</span>
			</div>
		{:else}
			<div class="raw nochild">
				<span on:click|stopPropagation={() => updateChart(task.id)} class="info-name">
					{task.name}
				</span>
			</div>
		{/if}
	</div>
{/each}
{#if modify}
	<div class="tree">
		<svelte:component this={ModalCreationTask} on:message bind:templates bind:model_id bind:task_id={parent_task_id} />
	</div>
{/if}
