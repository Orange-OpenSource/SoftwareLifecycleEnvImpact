import type { EnvironmentalImpact, Task } from '$lib/api/dataModel';

export interface D3JSNode {
	name: string;
	// value: number;
	co2: number
	impact: EnvironmentalImpact;
	children: D3JSNode[];
	task?: Task;
}
