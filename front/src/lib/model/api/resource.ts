import type { PatchDocument } from '$lib/model/api/model/patchDocument';
import { patch, post, del } from './api';
import type { ImpactSource, Resource } from './model/resource';
import { TIME_UNITS } from '$lib/model/api/model/resource';

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
	let duration;
	let input = { value: 1, unit: impact_source.unit }; // create the quantity
	// Check if time needed
	impact_source.unit.split(/[*,/]/).forEach(function (unit) {
		unit = unit.trim();
		if (TIME_UNITS.indexOf(unit) > -1) {
			duration = { value: 1, unit: unit }; // create the quantity for duration
		} else {
			input = { value: 1, unit: unit }; // redefine input quantity without duration
		}
	});

	const res = await post('resources', {
		task_id: taskId,
		impact_source_id: impact_source.id,
		input: input,
		duration: duration
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
	if (resource.time_use)
		patchDocument.push({
			op: 'replace',
			path: '/time_use',
			value: { value: resource.time_use.value, unit: resource.time_use.unit }
		});
	if (resource.frequency)
		patchDocument.push({
			op: 'replace',
			path: '/frequency',
			value: { value: resource.frequency.value, unit: resource.frequency.unit }
		});
	if (resource.duration)
		patchDocument.push({
			op: 'replace',
			path: '/duration',
			value: { value: resource.duration.value, unit: resource.duration.unit }
		});

	const res = await patch('resources/' + resource.id, patchDocument);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
