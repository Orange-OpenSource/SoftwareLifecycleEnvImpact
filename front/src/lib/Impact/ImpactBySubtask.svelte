<script lang="ts">
	import type { Task, SubtasksImpact } from '$lib/api/dataModel';
	import { hierarchy } from 'd3-hierarchy';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';

	export let impactBySubtask: SubtasksImpact;

	/*Bound var*/
	export let selectedTask: Task;

	function convertSubtasksImpactToHierarchy(): HierarchyNode {
		let final = {
			name: 'root',
			children: []
		};

		for (const [task_id, impact] of Object.entries(impactBySubtask)) {
			/*Retrieve task object from its id*/
			let task = selectedTask.subtasks.find((s) => s.id == Number(task_id))!;

			if (task != undefined) {
				if (impact.impacts['Climate change'] != undefined) {
					/**For each task push it with its associated impact*/
					final.children.push({
						name: task.name,
						value: impact.impacts['Climate change'].value
					});
				}
			}
		}
		return hierarchy(final);
	}
</script>

<Sunburst hierarchy={convertSubtasksImpactToHierarchy()} />
