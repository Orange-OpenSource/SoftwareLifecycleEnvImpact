import type { AggregatedImpact } from './impact';

export interface TaskImpact {
	task_id: number;
	task_impact: AggregatedImpact;
	subtasks: SubtasksImpact;
	resources: ResourcesImpact;
}

export type ResourcesImpact = Record<ResourceName, AggregatedImpact>;
export type SubtasksImpact = Record<Id, AggregatedImpact>;
export type Id = string;
export type ResourceName = string;
