import type { PatchDocument } from '$lib/model/api/model/patchDocument';
import { patch, post, del } from './api';
import type { Resource } from './model/resource';

export async function updateResourceRequest(resource: Resource, newValue: string): Promise<Resource> {
	const patchDocument: PatchDocument = {
		op: 'replace',
		path: '/value',
		value: newValue
	};
	const res = await patch('resources/' + resource.id, patchDocument);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function addResourceRequest(name: string, taskId: number, templateId: number) {
	const res = await post('resources', {
		name: name,
		task_id: taskId,
		template_id: templateId
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
