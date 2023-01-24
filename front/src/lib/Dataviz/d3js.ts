import { impactValueTotal, type EnvironmentalImpact, type ImpactSourceImpact, type Task, type TaskImpact } from '$lib/api/dataModel';

export interface D3JSHierarchyNode {
	name: string;
	// value: number;
	co2: number;
	impact: EnvironmentalImpact;
	children: D3JSHierarchyNode[];
	task?: Task;
}

export interface D3JSLink {
	source: string;
	target: string;
	value: number;
}

export interface D3JStackedData {
	impactCategory: string;
	category: string;
	value: number;
}

export function constructLinks(task: Task, impacts: TaskImpact[], showTasks = true, showResources = true): D3JSLink[] {
	let links: D3JSLink[] = [];
	constructSubLinksRecursive(links, task, impacts, showTasks, showResources);
	return links;
}

function constructSubLinksRecursive(links: D3JSLink[], parentTask: Task, taskImpacts: TaskImpact[], showTasks: boolean, showResources: boolean) {
	// Iterate through all subtasks
	for (const subtaskImpact of taskImpacts) {
		// Retrieve the sub task associated to the impact
		const subtask = parentTask.subtasks.find((s) => s.id == Number(subtaskImpact.task_id))!;

		if (subtask != undefined) {
			const value = impactValueTotal(subtaskImpact.total['Climate change']).value;
			if (value && showTasks)
				links.push({
					source: parentTask.name,
					target: subtask.name,
					value: value
				});

			// Iterate through impact by source to create links
			for (const [impactSourceId, impactSourceImpact] of Object.entries(subtaskImpact.impact_sources)) {
				// 	// If task has no subtasks, or that they do not use this impactSource, draw the links
				if (showResources && (subtask.subtasks.length == 0 || !subtasksContainsImpactSource(impactSourceId, subtask))) {
					constructSubResourcesLinks(links, impactSourceImpact, showTasks ? subtask.name : 'Total');
				}
				// }
			}

			// Recursive call for the subtask, and its subtasks
			constructSubLinksRecursive(links, subtask, subtaskImpact.sub_tasks, showTasks, showResources);
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
