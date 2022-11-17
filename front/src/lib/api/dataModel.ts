export interface Project {
	/**
	 * Unique identifier
	 */
	id: number;
	/**
	 * Name of the project
	 */
	name: string;
	/**
	 * List of the project models
	 */
	models?: Array<Model>;
	/**
	 * Creation date of the task
	 */
	created_at: string;
	/**
	 * Last update date of the task
	 */
	updated_at: string;
}

export interface Model {
	/**
	 * Unique identifier
	 */
	id: number;
	/**
	 * Name of the model
	 */
	name: string;
	/**
	 * Creation date of the model
	 */
	created_at: string;
	/**
	 * Last update date of the model
	 */
	updated_at: string;
	/**
	 * Model root task
	 */
	root_task: Task;
}

export interface Resource {
	[x: string]: {};
	id: number;
	name: string;
	impact_source_id: string;
	input: Quantity;
	has_time_input: boolean;
	duration?: Quantity;
	frequency?: Quantity;
	time_use?: Quantity;
	created_at: string;
	updated_at: string;
}

export interface Quantity {
	value: number;
	unit: string;
}

export interface ImpactSource {
	id: string;
	name: string;
	unit: string;
	source: string;
	methodology: string;
}

export const TIME_UNITS = ['minute', 'hour', 'day', 'month', 'year'];

export interface Task {
	/**
	 * Unique identifier
	 */
	id: number;
	/**
	 * Name of the task
	 */
	name: string;
	/**
	 * Resources associated to the task
	 */
	resources: Array<Resource>;
	/**
	 * Subtasks
	 */
	subtasks: Array<Task>;
	/**
	 * Creation date of the task
	 */
	created_at: string;
	/**
	 * Last update date of the task
	 */
	updated_at: string;
	/**
	 * Id of the parent task if it exists
	 */
	parent_task_id: number;
}

export interface TaskTemplate {
	/**
	 * Unique identifier
	 */
	id: number;
	/**
	 * Name of the task template
	 */
	name: string;
	/**
	 * Unit of the task
	 */
	unit: string;
	/**
	 * Resources
	 */
	resources: Array<Resource>;
}

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

/**
 * A JSONPatch document as defined by RFC 6902
 */
export interface PatchDocument {
	/**
	 * The operation to be performed
	 */
	op: OpEnum;
	/**
	 * A JSON-Pointer
	 */
	path: string;
	/**
	 * The value to be used within the operations.
	 */
	value: string | object;
}

export type OpEnum = 'merge' | 'remove' | 'replace' | 'move' | 'copy' | 'test';
