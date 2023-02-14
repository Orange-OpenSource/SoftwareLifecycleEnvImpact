import { impactValueTotal, type EnvironmentalImpact, type ImpactSourceId, type ImpactSourceImpact, type Quantity, type Task, type TaskImpact } from '$lib/api/dataModel';

export interface D3JSHierarchyNode {
	name: string;
	// value: number;
	manufacture: number;
	use: number;
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

export interface D3JGroupedData {
	resourceName: string;
	modelName: string;
	value: number;
}

export interface D3JsDivergingData {
	first: number;
	second: number;
	name: string;
}

export function constructLinks(selectedImpactCategory: string, task: Task, impact: TaskImpact, showTasks = true, showResources = true): D3JSLink[] {
	const links: D3JSLink[] = [];
	constructSubLinksRecursive(selectedImpactCategory, links, task, impact, showTasks, showResources);
	return links;
}

function constructSubLinksRecursive(selectedImpactCategory: string, links: D3JSLink[], task: Task, taskImpact: TaskImpact, showTasks: boolean, showResources: boolean) {
	// For each subtasks, create the link
	for (const subtaskImpact of taskImpact.sub_tasks) {
		// Retrieve the sub task associated to the impact
		const subtask = task.subtasks.find((s) => s.id == Number(subtaskImpact.task_id))!;

		if (subtask != undefined) {
			const total = subtaskImpact.total[selectedImpactCategory];
			if (showTasks) {
				if (total.use && total.use.value) {
					// Push use
					links.push({
						source: task.name,
						target: subtask.name,
						value: total.use.value
					});
				}
				// Push manufacture
				if (total.manufacture && total.manufacture.value) {
					links.push({
						source: task.name,
						target: subtask.name,
						value: total.manufacture.value
					});
				}
			}
			// Recursive call for the subtask, and its subtasks
			constructSubLinksRecursive(selectedImpactCategory, links, subtask, subtaskImpact, showTasks, showResources);
		}
	} // Iterate through impact by source to create links
	if (task.subtasks.length == 0) {
		for (const [_, impactSourceImpact] of Object.entries(taskImpact.impact_sources)) {
			// Draw resources impact links if needed
			if (showResources) {
				constructResourcesLinks(selectedImpactCategory, links, impactSourceImpact, showTasks ? task.name : 'Total');
			}
		}
	}
}

function sumSubimpacts(selectedImpactCategory, sub_impacts: Record<ImpactSourceId, ImpactSourceImpact>) {
	let sum = 0;
	for (const [_, subImpact] of Object.entries(sub_impacts)) {
		const total = impactValueTotal(subImpact.own_impact[selectedImpactCategory]).value;
		if (total) {
			sum += total;
		}
		sum += sumSubimpacts(selectedImpactCategory, subImpact.sub_impacts);
	}
	return sum;
}

function constructResourcesLinks(selectedImpactCategory: string, links: D3JSLink[], resourceImpact: ImpactSourceImpact, parentName: string) {
	// If this resourceImpact has an own impact, push it toward the parentName
	const total = impactValueTotal(resourceImpact.own_impact[selectedImpactCategory]).value;
	if (total) {
		links.push({
			source: parentName,
			target: resourceImpact.impact_source_id,
			value: total
		});
	}

	// Push toward the parentName all this resource subImpacts values
	links.push({
		source: parentName,
		target: resourceImpact.impact_source_id,
		value: sumSubimpacts(selectedImpactCategory, resourceImpact.sub_impacts)
	});

	// Iterate through all of this subtasks to draw its impact toward
	for (const [_, subImpact] of Object.entries(resourceImpact.sub_impacts)) {
		const own_impact = resourceImpact.own_impact[selectedImpactCategory];
		// Push the resourceImpact manufacture towards manufacture
		if (own_impact.manufacture && own_impact.manufacture.value) {
			links.push({
				source: resourceImpact.impact_source_id,
				target: 'Manufacture',
				value: own_impact.manufacture.value
			});
		}
		// Recursive call for childrens
		constructResourcesLinks(selectedImpactCategory, links, subImpact, resourceImpact.impact_source_id);
	}

	// If there isn't subtasks, draw to use and manufacture directly
	if (Object.entries(resourceImpact.sub_impacts).length == 0) {
		const total = resourceImpact.own_impact[selectedImpactCategory];
		// Push use
		if (total.use && total.use.value) {
			links.push({
				source: resourceImpact.impact_source_id,
				target: 'Use',
				value: total.use.value
			});
		}
		// Push manufacture
		if (total.manufacture && total.manufacture.value) {
			links.push({
				source: resourceImpact.impact_source_id,
				target: 'Manufacture',
				value: total.manufacture.value
			});
		}
	}
}
