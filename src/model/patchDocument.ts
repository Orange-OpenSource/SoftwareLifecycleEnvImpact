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
	value: string;
}

export type OpEnum = 'merge' | 'remove' | 'replace' | 'move' | 'copy' | 'test';
