<script lang="ts">
	import { getModelImpact } from '$lib/controllers/RequestController';
	import { onMount } from 'svelte';

	export let CURRENT_MODEL_ID: any;
	export let subtasks: any;
	export let modify: any;
	export let parent_task_id: any;
	export let tasks: any[];
	export let templates: any;
	export let myChart: any;

	let ModalCreationTask: any;
	let ModalModifyTask: any;

	/**
	 * Update the chart with the new data.
	 */
	async function updateChart(task: any) {
		let labels = [];
		let data = [];
		let res: any = await getModelImpact(CURRENT_MODEL_ID);
		let dict: any = {};

		function pushEachTaskAndImpactIntoDict(array: any) {
			dict[array.task.id] = array.environmental_impact;

			for (let i = 0; i < array.subtasks_impacts.length; i++) pushEachTaskAndImpactIntoDict(array.subtasks_impacts[i]);
		}

		pushEachTaskAndImpactIntoDict(res);

		if (task.subtasks.length) {
			for (let i in task.subtasks) {
				if (Object.keys(dict[task.subtasks[i].id]).length) {
					let climate_change = dict[task.subtasks[i].id]['Climate change'].split(' ')[0];
					data.push(+climate_change);
					labels.push(task.subtasks[i].name);
				}
			}
		} else {
			if (Object.keys(dict[task.id]).length) {
				let climate_change = dict[task.id]['Climate change'].split(' ')[0];
				data.push(+climate_change);
				labels.push(task.name);
			}
		}

		labels = labels;
		data = data;

		myChart.data.labels = labels;
		myChart.data.datasets[0].data = data;
		myChart.update();
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
				<span on:click|stopPropagation={() => updateChart(task)} class="info-name">
					{task.name}
					{#if modify}
						<svelte:component this={ModalModifyTask} on:message bind:tasks bind:templates {task} classAttribute={'btnmodifyparent'} />
					{/if}
				</span>

				<svelte:self on:message subtasks={task.subtasks} bind:templates bind:myChart bind:modify parent_task_id={task.id} {CURRENT_MODEL_ID} {tasks} />
			</div>
		{:else if modify}
			<div class="raw nochildmodify">
				<span on:click|stopPropagation={() => updateChart(task)} class="info-name">
					{task.name}
					<svelte:component this={ModalModifyTask} on:message bind:tasks bind:templates {task} classAttribute={'btnmodify'} />
				</span>
				<span class="addtask">
					<svelte:component this={ModalCreationTask} on:message bind:templates bind:CURRENT_MODEL_ID bind:task_id={task.id} />
				</span>
			</div>
		{:else}
			<div class="raw nochild">
				<span on:click|stopPropagation={() => updateChart(task)} class="info-name">
					{task.name}
				</span>
			</div>
		{/if}
	</div>
{/each}
{#if modify}
	<div class="tree">
		<svelte:component this={ModalCreationTask} on:message bind:templates bind:CURRENT_MODEL_ID bind:task_id={parent_task_id} />
	</div>
{/if}
