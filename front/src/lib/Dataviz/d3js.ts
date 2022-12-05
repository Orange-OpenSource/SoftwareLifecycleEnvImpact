import type { EnvironmentalImpact } from "$lib/api/dataModel";
import type Task from "$lib/Task/Task.svelte";

export interface D3JSNode {
	name: string;
    task?: Task,
	value?: number;
	impact?: EnvironmentalImpact;
	children: D3JSNode[];
}
