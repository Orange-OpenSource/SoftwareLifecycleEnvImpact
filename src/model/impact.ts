export interface Impact {
	unit: string;
	value: number;
}
export type ImpactName = string;
export type AggregatedImpact = Record<ImpactName, Impact>;
