import { impactValueTotal, type EnvironmentalImpact, type ImpactSourceImpact, type Activity, type ActivityImpact } from '$lib/api/dataModel';

export interface D3JSHierarchyNode {
	name: string;
	// value: number;
	manufacture: number;
	use: number;
	impact: EnvironmentalImpact;
	children: D3JSHierarchyNode[];
	activity?: Activity;
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

export function constructLinks(selectedImpactCategory: string, activity: Activity, impact: ActivityImpact, showActivities = true, showResources = true): D3JSLink[] {
	const links: D3JSLink[] = [];
	constructSubLinksRecursive(selectedImpactCategory, links, activity, impact, showActivities, showResources);
	return links;
}

function constructSubLinksRecursive(selectedImpactCategory: string, links: D3JSLink[], activity: Activity, activityImpact: ActivityImpact, showActivities: boolean, showResources: boolean) {
	// For each subactivities, create the link
	for (const subactivityImpact of activityImpact.sub_activities) {
		// Retrieve the sub activity associated to the impact
		const subactivity = activity.subactivities.find((s) => s.id == Number(subactivityImpact.activity_id))!;

		if (subactivity != undefined) {
			const total = subactivityImpact.total[selectedImpactCategory];
			if (showActivities) {
				if (total.use && total.use.value) {
					// Push use
					links.push({
						source: activity.name,
						target: subactivity.name,
						value: total.use.value
					});
				}
				// Push manufacture
				if (total.manufacture && total.manufacture.value) {
					links.push({
						source: activity.name,
						target: subactivity.name,
						value: total.manufacture.value
					});
				}
			}
			// Recursive call for the subactivity, and its subactivities
			constructSubLinksRecursive(selectedImpactCategory, links, subactivity, subactivityImpact, showActivities, showResources);
		}
	} // Iterate through impact by source to create links
	if (activity.subactivities.length == 0) {
		for (const [_, impactSourceImpact] of Object.entries(activityImpact.impact_sources)) {
			// Draw resources impact links if needed
			if (showResources) {
				constructResourcesLinks(selectedImpactCategory, links, impactSourceImpact, showActivities ? activity.name : 'Total');
			}
		}
	}
}

function constructResourcesLinks(selectedImpactCategory: string, links: D3JSLink[], resourceImpact: ImpactSourceImpact, parentName: string) {
	// If this resourceImpact has a total imapct, push it toward the parentName
	const total = impactValueTotal(resourceImpact.total_impact[selectedImpactCategory]).value;
	if (total) {
		links.push({
			source: parentName,
			target: resourceImpact.impact_source_id,
			value: total
		});
	}

	// Iterate through all of this subactivities to draw its impact toward
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

	// If there isn't subactivities, draw to use and manufacture directly
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
