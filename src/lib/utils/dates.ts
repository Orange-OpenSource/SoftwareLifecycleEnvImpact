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

export function getCreationDate(ISODate: any) {
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
