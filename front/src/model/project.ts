import type { Model } from './model';

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
