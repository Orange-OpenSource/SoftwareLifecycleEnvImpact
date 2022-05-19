/**
 * Returns the last updated date (or creation date if null).
 *
 * @param model the model with `created_at` and `updated_at` fields.
 * @returns 	the date under format : DD/MM/YYYY XX:XX
 */
export function getLastUpdate(model: any) {
	let date;

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

/**
 * Returns the creation date.
 *
 * @param ISODate 	the date in ISO format.
 * @returns 		the date under format : DD/MM/YYYY XX:XX
 */
export function getCreationDate(ISODate: string) {
	let date = new Date(ISODate);

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
