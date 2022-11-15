export interface Resource {
	[x: string]: {};
	id: number;
	name: string;
	impact_source_id: string;
	input: Quantity;
	has_time_input: boolean;
	duration?: Quantity;
	frequency?: Quantity;
	time_use?: Quantity;
	created_at: string;
	updated_at: string;
}

export interface Quantity {
	value: number;
	unit: string;
}

export interface ImpactSource {
	id: string;
	name: string;
	unit: string;
	source: string;
	methodology: string;
}

export const TIME_UNITS = ['minute', 'hour', 'day', 'month', 'year'];
