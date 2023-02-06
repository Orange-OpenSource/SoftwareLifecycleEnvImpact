import type { Model } from '$lib/api/dataModel';
import type { Project } from '$lib/api/dataModel';

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

export function exportJson(data: string, fileName: string) {
	//Used to generate file only on click
	if (data == null || !data.length) {
		return null;
	}

	const blob = new Blob([data]);
	const link = document.createElement('a');
	if (link.download !== undefined) {
		const url = URL.createObjectURL(blob);
		link.setAttribute('href', url);
		link.setAttribute('download', fileName + '.json');
		link.style.visibility = 'hidden';
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
}

export function exportSvg(data: string, fileName: string) {
	//Used to generate file only on click
	if (data == null || !data.length) {
		return null;
	}

	const blob = new Blob([data]);
	const link = document.createElement('a');
	if (link.download !== undefined) {
		const url = URL.createObjectURL(blob);
		link.setAttribute('href', url);
		link.setAttribute('download', fileName + '.svg');
		link.style.visibility = 'hidden';
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
}
