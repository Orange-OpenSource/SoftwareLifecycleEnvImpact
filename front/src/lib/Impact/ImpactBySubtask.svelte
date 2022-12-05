<script lang="ts">
	import type { Task, TaskImpact } from '$lib/api/dataModel';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import type { D3JSNode } from '$lib/Dataviz/d3js';

	export let impactBySubtask: TaskImpact[];

	/*Bound var*/
	export let selectedTask: Task;

	$: subtaskHierarchy = hierarchy({
		name: 'root',
		children: getChildrenNodes(selectedTask, impactBySubtask)
	});

	function getChildrenNodes(parentTask: Task, taskImpacts: TaskImpact[]): D3JSNode[] {
		let returnValue = [];
		for (const taskImpact of taskImpacts) {
			/*Retrieve task object from its id*/
			let task = parentTask.subtasks.find((s) => s.id == Number(taskImpact.task_id))!;

			if (task != undefined) {
				// If retrieved, create node
				if (taskImpact.task_impact.impacts['Climate change'] != undefined) {
					/**For each task push it with its associated impact*/
					returnValue.push({
						name: task.name,
						value: taskImpact.task_impact.impacts['Climate change'].value,
						children: getChildrenNodes(task, taskImpact.subtasks),
					});
				}
			}
		}
		return returnValue;
	}
</script>

<Sunburst hierarchy={subtaskHierarchy} />
