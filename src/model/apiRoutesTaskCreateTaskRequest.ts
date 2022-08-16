export interface ApiRoutesTaskCreateTaskRequest {
	/**
	 * Name of the task
	 */
	name: string;
	/**
	 * Id of the related Model
	 */
	model_id: number;
	/**
	 * Parent task id
	 */
	parent_task_id: number;
	/**
	 * Id of the template to create from
	 */
	template_id: number;
}
