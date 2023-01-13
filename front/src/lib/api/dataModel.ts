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
	id: number;
	name: string;
	impact_source_id: string;
	amount: Quantity;
	has_time_input: boolean;
	period: Quantity;
	frequency: Quantity;
	duration: Quantity;
	created_at: string;
	updated_at: string;
}

export interface Quantity {
	value?: number;
	unit?: string;
}

export interface ImpactSource {
	id: string;
	name: string;
	unit: string;
	source: string;
	methodology: string;
}

export const TIME_UNITS = ['minute', 'hour', 'day', 'week', 'month', 'year'];

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

export interface ImpactValue {
	manufacture?: Quantity;
	use?: Quantity;
}

// Not a method of an ImpactValue class as Js cannot directly map JSON to objects
export function impactValueTotal(impactValue: ImpactValue): Quantity {
	if (impactValue.manufacture && impactValue.manufacture.value && impactValue.use && impactValue.use.value) {
		return {
			value: impactValue.manufacture.value + impactValue.use.value,
			unit: impactValue.manufacture.unit
		};
	} else if (impactValue.manufacture && impactValue.manufacture.value && impactValue.manufacture.unit) {
		return {
			value: impactValue.manufacture.value,
			unit: impactValue.manufacture.unit
		};
	} else if (impactValue.use && impactValue.use.value && impactValue.use.unit) {
		return {
			value: impactValue.use.value,
			unit: impactValue.use.unit
		};
	}
	return {};
}

export type ImpactName = string; // TODO should have an enum associated
export type EnvironmentalImpact = Record<ImpactName, ImpactValue>;

export type ImpactSourceId = string;
export type ImpactSourcesImpact = Record<ImpactSourceId, EnvironmentalImpact>;

export interface ImpactSourceImpact {
	impact_source_id: string;
	total: EnvironmentalImpact;
	sub_impacts: Record<ImpactSourceId, ImpactSourceImpact>;
}

export interface TaskImpact {
	task_id: number;
	total: EnvironmentalImpact;
	sub_tasks: TaskImpact[];
	impact_sources: Record<ImpactSourceId, ImpactSourceImpact>;
}

export type Id = string;
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
