<script lang="ts">
	import { type Task, type TaskImpact } from '$lib/api/dataModel';
	import { hierarchy } from 'd3-hierarchy';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import { constructLinks, type D3JSHierarchyNode } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';

	export let impact: TaskImpact;
	export let selectedImpactCategory: string;

	/*Bound var*/
	export let selectedTask: Task;

	$: subtaskHierarchy = constructHierarchy(selectedImpactCategory);
	$: subtasksLinks = constructLinks(selectedImpactCategory, selectedTask, impact, true, false);

	function constructHierarchy(name: string) {
		return hierarchy({
			name: name,
			children: getHierarchyChildrenNodes(selectedTask, impact.sub_tasks)
		});
	}

	function getHierarchyChildrenNodes(parentTask: Task, taskImpacts: TaskImpact[]): D3JSHierarchyNode[] {
		let returnValue: D3JSHierarchyNode[] = [];
		for (const taskImpact of taskImpacts) {
			/*Retrieve task object from its id*/
			let task = parentTask.subtasks.find((s) => s.id == Number(taskImpact.task_id))!;

			if (task != undefined) {
				// If retrieved, create node
				if (taskImpact.total[selectedImpactCategory] != undefined) {
					/**For each task push it with its associated impact*/
					const total = taskImpact.total[selectedImpactCategory];
					const manufacture = total.manufacture && total.manufacture.value ? total.manufacture.value : 0;
					const use = total.use && total.use.value ? total.use.value : 0;
					if (total) {
						returnValue.push({
							name: task.name,
							task: task,
							impact: taskImpact.total,
							manufacture: manufacture,
							use: use,
							children: getHierarchyChildrenNodes(task, taskImpact.sub_tasks)
						});
					}
				}
			}
		}
		return returnValue;
	}
</script>

{#if impact.sub_tasks.length > 0}
	<div class="row">
		<h3>Subtasks:</h3>
	</div>
	<Sunburst bind:selectedTask hierarchy={subtaskHierarchy} />
	<Sankey links={subtasksLinks} />
{/if}
