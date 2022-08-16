export interface ApiRoutesResourceCreateResourceRequest {
	/**
	 * Name of the resource
	 */
	name: string;
	/**
	 * Id of the task to create the resource in
	 */
	task_id: number;
	/**
	 * Id of the template to create from
	 */
	template_id: number;
}
