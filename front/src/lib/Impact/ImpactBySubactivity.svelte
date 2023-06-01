<script lang="ts">
	import { type Activity, type ActivityImpact } from '$lib/api/dataModel';
	import { hierarchy } from 'd3-hierarchy';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import { constructLinks, type D3JSHierarchyNode } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';

	export let impact: ActivityImpact;
	export let selectedImpactCategory: string;

	/*Bound var*/
	export let selectedActivity: Activity;

	$: subactivityHierarchy = constructHierarchy(selectedImpactCategory);
	$: subactivitiesLinks = constructLinks(selectedImpactCategory, selectedActivity, impact, true, false);

	function constructHierarchy(name: string) {
		return hierarchy({
			name: name,
			children: getHierarchyChildrenNodes(selectedActivity, impact.sub_activities)
		});
	}

	function getHierarchyChildrenNodes(parentActivity: Activity, activityImpacts: ActivityImpact[]): D3JSHierarchyNode[] {
		let returnValue: D3JSHierarchyNode[] = [];
		for (const activityImpact of activityImpacts) {
			/*Retrieve activity object from its id*/
			let activity = parentActivity.subactivities.find((s) => s.id == Number(activityImpact.activity_id))!;

			if (activity != undefined) {
				// If retrieved, create node
				if (activityImpact.total[selectedImpactCategory] != undefined) {
					/**For each activity push it with its associated impact*/
					const total = activityImpact.total[selectedImpactCategory];
					const manufacture = total.manufacture && total.manufacture.value ? total.manufacture.value : 0;
					const use = total.use && total.use.value ? total.use.value : 0;
					if (total) {
						returnValue.push({
							name: activity.name,
							activity: activity,
							impact: activityImpact.total,
							manufacture: manufacture,
							use: use,
							children: getHierarchyChildrenNodes(activity, activityImpact.sub_activities)
						});
					}
				}
			}
		}
		return returnValue;
	}
</script>

{#if impact.sub_activities.length > 0}
	<div class="row">
		<h3>Subactivities:</h3>
	</div>
	<Sunburst bind:selectedActivity hierarchy={subactivityHierarchy} />
	<Sankey links={subactivitiesLinks} />
{/if}
