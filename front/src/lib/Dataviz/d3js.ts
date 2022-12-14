import type { EnvironmentalImpact, Task } from '$lib/api/dataModel';

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
