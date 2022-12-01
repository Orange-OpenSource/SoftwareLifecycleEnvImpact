import { type PatchDocument, type ImpactSource, type Resource, TIME_UNITS } from '$lib/api/dataModel';
import { patch, post, del } from './api';

export async function renameResourceRequest(resource: Resource, newName: string): Promise<Resource> {
	const patchDocument: PatchDocument = {
		op: 'replace',
		path: '/name',
		value: newName
	};
	const res = await patch('resources/' + resource.id, [patchDocument]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function addResourceRequest(taskId: number, impact_source: ImpactSource) {
	let period;
	let input = { value: 1, unit: impact_source.unit }; // create the quantity
	// Check if time needed
	impact_source.unit.split(/[*,/]/).forEach(function (unit) {
		unit = unit.trim();
		if (TIME_UNITS.indexOf(unit) > -1) {
			period = { value: 1, unit: unit }; // create the quantity for period
		} else {
			input = { value: 1, unit: unit }; // redefine input quantity without period
		}
	});

	const res = await post('resources', {
		name: impact_source.name,
		task_id: taskId,
		impact_source_id: impact_source.id,
		input: input,
		period: period
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function deleteResourceRequest(resource: Resource): Promise<Resource> {
	const res = await del('resources/' + resource.id);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function updateResourceInputRequest(resource: Resource): Promise<Resource> {
	const patchDocument: PatchDocument[] = [
		{
			op: 'replace',
			path: '/input',
			value: { value: resource.input.value, unit: resource.input.unit }
		}
	];
	if (resource.time_use && resource.time_use.value != undefined && resource.time_use.unit != undefined)
		patchDocument.push({
			op: 'replace',
			path: '/time_use',
			value: { value: resource.time_use.value, unit: resource.time_use.unit }
		});
	if (resource.frequency && resource.frequency.value != undefined && resource.frequency.unit != undefined)
		patchDocument.push({
			op: 'replace',
			path: '/frequency',
			value: { value: resource.frequency.value, unit: resource.frequency.unit }
		});
	if (resource.period && resource.period.value != undefined && resource.period.unit != undefined)
		patchDocument.push({
			op: 'replace',
			path: '/period',
			value: { value: resource.period.value, unit: resource.period.unit }
		});

	try {
		const res = await patch('resources/' + resource.id, patchDocument);
		return res.text().then((json: string) => {
			return JSON.parse(json);
		});
	} catch (e) {
		return Promise.reject({
			errors: JSON.parse(e.message)
		});
	}
}
