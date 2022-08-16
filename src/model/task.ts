import type { Resource } from './resource';

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
