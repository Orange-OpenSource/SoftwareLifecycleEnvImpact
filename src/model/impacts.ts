/**
 * Impact quantity
 */
export interface Impact {
	/*Impact unit */
	unit: string;
	/*Impact value*/
	value: number;
}

export type ImpactName = string;
/**
 * Dict of impacts by impact name
 */
export type AggregatedImpact = Record<ImpactName, Impact>;

/**
 * All environmental impacts for a task
 */
export interface TaskImpact {
	/**
	 * Id of the corresponding task
	 */
	task_id: number;
	/**
	 * Aggregated impact for this task
	 */
	task_impact: AggregatedImpact;
	/**
	 * All task subtask's impacts
	 */
	subtasks: SubtasksImpact;
	/**
	 * Task impact by resource name
	 */
	resources: ResourcesImpact;
}

export type ResourceName = string;
/**
 * Dict of aggregated impact by resource name
 */
export type ResourcesImpact = Record<ResourceName, AggregatedImpact>;

export type Id = string;
/**
 * Dict of aggregated impact by subtask id
 */
export type SubtasksImpact = Record<Id, AggregatedImpact>;
