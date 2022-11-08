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

export async function addResourceRequest(name: string, taskId: number, impact_source: ImpactSource) {
	let duration;
	let input = '1 ' + impact_source.unit; // create the quantity
	// Check if time needed
	impact_source.unit.split(/[*,/]/).forEach(function (unit) {
		unit = unit.trim()
		if (TIME_UNITS.indexOf(unit) > -1) {
			duration = '1 ' + unit; // create the quantity for duration
		} else {
			input = '1 ' + unit; // redefine input quantity without duration
		}
	});
	
	const res = await post('resources', {
		name: name,
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
			value: resource.input.value + ' ' + resource.input.unit
		},
		{
			op: 'replace',
			path: '/time_use',
			value: resource.time_use.value + ' ' + resource.time_use.unit
		},
		{
			op: 'replace',
			path: '/frequency',
			value: resource.frequency.value + ' ' + resource.frequency.unit
		},
		{
			op: 'replace',
			path: '/duration',
			value: resource.duration.value + ' ' + resource.duration.unit
		}
	];
	const res = await patch('resources/' + resource.id, patchDocument);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
