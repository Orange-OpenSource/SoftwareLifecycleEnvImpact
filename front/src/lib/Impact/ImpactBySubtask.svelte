<script lang="ts">
	import { impactValueTotal, type ImpactSourceImpact, type Task, type TaskImpact } from '$lib/api/dataModel';
	import { hierarchy } from 'd3-hierarchy';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import type { D3JSLink, D3JSHierarchyNode } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';

	export let impactBySubtask: TaskImpact[];
	export let selectedImpactName: string;

	/*Bound var*/
	export let selectedTask: Task;

	$: subtaskHierarchy = constructHierarchy(selectedImpactName);
	$: subtasksLinks = constructLinks();

	function constructHierarchy(name: string) {
		return hierarchy({
			name: name,
			children: getHierarchyChildrenNodes(selectedTask, impactBySubtask)
		});
	}

	function getHierarchyChildrenNodes(parentTask: Task, taskImpacts: TaskImpact[]): D3JSHierarchyNode[] {
		let returnValue: D3JSHierarchyNode[] = [];
		for (const taskImpact of taskImpacts) {
			/*Retrieve task object from its id*/
			let task = parentTask.subtasks.find((s) => s.id == Number(taskImpact.task_id))!;

			if (task != undefined) {
				// If retrieved, create node
				if (taskImpact.total[selectedImpactName] != undefined) {
					/**For each task push it with its associated impact*/
					const total = impactValueTotal(taskImpact.total[selectedImpactName]).value;
					if (total) {
						returnValue.push({
							name: task.name,
							task: task,
							impact: taskImpact.total,
							// value: taskImpact.task_impact['Climate change'].value,
							co2: total,
							children: getHierarchyChildrenNodes(task, taskImpact.sub_tasks)
						});
					}
				}
			}
		}
		return returnValue;
	}

	function constructSubLinksRecursive(links: D3JSLink[], parentTask: Task, taskImpacts: TaskImpact[]) {
		// Iterate through all subtasks
		for (const subtaskImpact of taskImpacts) {
			// Retrieve the sub task associated to the impact
			let subtask = parentTask.subtasks.find((s) => s.id == Number(subtaskImpact.task_id))!;

			if (subtask != undefined) {
				const value = impactValueTotal(subtaskImpact.total['Climate change']).value;
				if (value)
					links.push({
						source: parentTask.name,
						target: subtask.name,
						value: value
					});

				// Iterate through impact by source to create links
				for (const [impactSourceId, impactSourceImpact] of Object.entries(subtaskImpact.impact_sources)) {
					// 	// If task has no subtasks, or that they do not use this impactSource, draw the links
					if (subtask.subtasks.length == 0 || !subtasksContainsImpactSource(impactSourceId, subtask)) {
						constructSubResourcesLinks(links, impactSourceImpact, subtask.name);
					}
					// }
				}

				// Recursive call for the subtask, and its subtasks
				constructSubLinksRecursive(links, subtask, subtaskImpact.sub_tasks);
			}
		}
	}

	function constructSubResourcesLinks(links: D3JSLink[], resourceImpact: ImpactSourceImpact, parentResourceName: string) {
		const value = impactValueTotal(resourceImpact.total['Climate change']).value;
		if (value)
			links.push({
				source: parentResourceName,
				target: resourceImpact.impact_source_id,
				value: value
			});
		for (const [_, subImpact] of Object.entries(resourceImpact.sub_impacts)) {
			constructSubResourcesLinks(links, subImpact, resourceImpact.impact_source_id);
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

{#if impactBySubtask.length > 0}
	<Sunburst bind:selectedTask hierarchy={subtaskHierarchy} />
	<Sankey links={subtasksLinks} />
{/if}
