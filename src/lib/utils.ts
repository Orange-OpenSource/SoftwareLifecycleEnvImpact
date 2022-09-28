import type { Model } from 'src/model/model';
import type { Project } from 'src/model/project';

/**
 * Returns the last updated date (or creation date if null).
 *
 * @param model the model or project with `created_at` and `updated_at` fields.
 * @returns 	the date under format : DD/MM/YYYY XX:XX
 */
export function getLastUpdate(model: Model | Project) {
	let date: Date;

	if (model.updated_at) {
		date = new Date(model.updated_at);
	} else {
		date = new Date(model.created_at);
	}

	return (
		(date.getDate() < 10 ? '0' : '') +
		date.getDate() +
		'/' +
		(date.getMonth() + 1 < 10 ? '0' : '') +
		(date.getMonth() + 1) +
		'/' +
		date.getFullYear() +
		' ' +
		(date.getHours() + 2) +
		':' +
		(date.getMinutes() < 10 ? '0' : '') +
		date.getMinutes()
	);
}
