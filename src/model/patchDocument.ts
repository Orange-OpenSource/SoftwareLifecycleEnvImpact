/**
 * A JSONPatch document as defined by RFC 6902
 */
export interface PatchDocument {
	/**
	 * The operation to be performed
	 */
	op: PatchDocument.OpEnum;
	/**
	 * A JSON-Pointer
	 */
	path: string;
	/**
	 * The value to be used within the operations.
	 */
	value: string;
}
export namespace PatchDocument {
	export type OpEnum = 'merge_aggregated_impact' | 'remove' | 'replace' | 'move' | 'copy' | 'test';
	export const OpEnum = {
		MergeAggregatedImpact: 'merge_aggregated_impact' as OpEnum,
		Remove: 'remove' as OpEnum,
		Replace: 'replace' as OpEnum,
		Move: 'move' as OpEnum,
		Copy: 'copy' as OpEnum,
		Test: 'test' as OpEnum
	};
}
