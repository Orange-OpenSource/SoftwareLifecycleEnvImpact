export interface Resource {
	/**
	 * Unique identifier
	 */
	id: number;
	/**
	 * Name of the resource
	 */
	name: string;
	/**
	 * Type of the resource
	 */
	type: string;
	/**
	 * Value of the resource
	 */
	value: number;
	/**
	 * Creation date of the resource
	 */
	created_at: string;
	/**
	 * Last update date of the resource
	 */
	updated_at: string;
}

export interface ResourceTemplate {
	/**
	 * Unique identifier
	 */
	id: number;
	/**
	 * Name of the resource
	 */
	name: string;
}