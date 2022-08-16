import type { Task } from './task';

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
