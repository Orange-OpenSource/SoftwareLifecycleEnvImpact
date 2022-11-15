/**
 * Impact quantity
 */
export interface Impact {
	/*Impact unit */
	unit: string;
	/*Impact value*/
	value: number;
}

export type ImpactName = string; // TODO should have an enum associated
/**
 * Dict of impacts by impact name
 */
export interface EnvironmentalImpact {
	// Impacts
	impacts: Record<ImpactName, Impact>;
}

/**
 * All environmental impacts for a task
 */
export interface TaskImpact {
	/**
	 * Id of the corresponding task
	 */
	task_id: number;
	/**
	 * Environmental impact for this task
	 */
	task_impact: EnvironmentalImpact;
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
 * Dict of environmental impact by resource name
 */
export type ResourcesImpact = Record<ResourceName, EnvironmentalImpact>;

export type Id = string;
/**
 * Dict of environmental impact by subtask id
 */
export type SubtasksImpact = Record<Id, EnvironmentalImpact>;
