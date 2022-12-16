<script lang="ts">
	import type { Task, TaskImpact } from '$lib/api/dataModel';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import type { D3JSLink, D3JSHierarchyNode } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';
	import Task from '$lib/Task/Task.svelte';

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
				/*Add a link for each resource*/
				for (const [resourceName, resourceImpact] of Object.entries(taskImpact.resources)) {
					// For each resource, add a link from parent to task
					links.push({
						source: parentTask.name,
						target: task.name,
						value: resourceImpact.impacts['Climate change'].value
					});
					// If task has no subtasks, then make the link to resources nodes
					// Make link to root node also if subtasks does not contains the impactsource
					if (task.subtasks.length == 0 || !subtasksContainsImpactSource(resourceName, task))
						links.push({
							source: task.name,
							target: resourceName,
							value: resourceImpact.impacts['Climate change'].value
						});
				}

				// Recursive call
				constructSubLinksRecursive(links, task, taskImpact.subtasks);
			}
		}
	}

	function subtasksContainsImpactSource(impactSourceId: string, task: Task) {
		// Recursive function on a task and its subtasks to check if it contains a resource id
		let returnValue = false;
		task.subtasks.forEach((subtask) => {
			// Check for each resource
			subtask.resources.forEach((resource) => {
				if (resource.impact_source_id == impactSourceId) returnValue = true;
			});
			// Recursive call
			if (subtasksContainsImpactSource(impactSourceId, subtask)) returnValue = true;
		});
		return returnValue;
	}
	function constructLinks(): D3JSLink[] {
		let links: D3JSLink[] = [];
		constructSubLinksRecursive(links, selectedTask, impactBySubtask);
		return links;
	}
</script>

<Sunburst bind:selectedTask hierarchy={subtaskHierarchy} />
<Sankey links={subtasksLinks} />
