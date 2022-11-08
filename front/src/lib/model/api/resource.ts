import type { PatchDocument } from '$lib/model/api/model/patchDocument';
import { patch, post, del } from './api';
import type { Resource } from './model/resource';

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

export async function addResourceRequest(name: string, taskId: number, impact_id: string) {
	const res = await post('resources', {
		name: name,
		task_id: taskId,
		impact_source_id: impact_source_id
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
			value: resource.input.toString()
		},
		{
			op: 'replace',
			path: '/days',
			value: resource.days.toString()
		},
		{
			op: 'replace',
			path: '/months',
			value: resource.months.toString()
		},
		{
			op: 'replace',
			path: '/years',
			value: resource.years.toString()
		}
	];
	const res = await patch('resources/' + resource.id, patchDocument);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}