<script lang="ts">
	import type { Task, TaskImpact } from '$lib/api/dataModel';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import type { D3JSLink, D3JSHierarchyNode } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';

	export let impactBySubtask: TaskImpact[];

	/*Bound var*/
	export let selectedTask: Task;

	$: subtaskHierarchy = hierarchy({
		name: 'root',
		children: getHierarchyChildrenNodes(selectedTask, impactBySubtask)
	});

	$: subtasksLinks = constructLinks();

	function getHierarchyChildrenNodes(parentTask: Task, taskImpacts: TaskImpact[]): D3JSHierarchyNode[] {
		let returnValue: D3JSHierarchyNode[] = [];
		for (const taskImpact of taskImpacts) {
			/*Retrieve task object from its id*/
			let task = parentTask.subtasks.find((s) => s.id == Number(taskImpact.task_id))!;

			if (task != undefined) {
				// If retrieved, create node
				if (taskImpact.task_impact.impacts['Climate change'] != undefined) {
					/**For each task push it with its associated impact*/
					returnValue.push({
						name: task.name,
						task: task,
						impact: taskImpact.task_impact,
						// value: taskImpact.task_impact.impacts['Climate change'].value,
						co2: taskImpact.task_impact.impacts['Climate change'].value,
						children: getHierarchyChildrenNodes(task, taskImpact.subtasks)
					});
				}
			}
		}
		return returnValue;
	}

	function constructSubLinksRecursive(links: D3JSLink[], parentTask: Task, taskImpacts: TaskImpact[]) {
		for (const taskImpact of taskImpacts) {
			/*Retrieve task object from its id*/
			let task = parentTask.subtasks.find((s) => s.id == Number(taskImpact.task_id))!;

			if (task != undefined) {
				// If retrieved, create node
				links.push({
					source: parentTask.name,
					target: task.name,
					value: taskImpact.task_impact.impacts['Climate change'].value
				});

				/*Add for each impact*/
				for (const [resourceName, resourceImpact] of Object.entries(taskImpact.resources)) {
					links.push({
						source: parentTask.name,
						target: resourceName,
						value: resourceImpact.impacts['Climate change'].value
					});
				}

				// Recursive call
				constructSubLinksRecursive(links, task, taskImpact.subtasks);
			}
		}
	}

	function constructLinks(): D3JSLink[] {
		let links: D3JSLink[] = [];
		constructSubLinksRecursive(links, selectedTask, impactBySubtask);
		return links;
	}
</script>

<Sankey links={subtasksLinks} />
<Sunburst bind:selectedTask hierarchy={subtaskHierarchy} />
