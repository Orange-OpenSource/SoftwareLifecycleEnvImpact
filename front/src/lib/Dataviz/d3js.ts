import type { EnvironmentalImpact } from "$lib/api/dataModel";

export interface D3JSNode {
	name: string;
	value?: number;
	impact?: EnvironmentalImpact;
	children: D3JSNode[];
}
