import type { Resource } from './resource';

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
