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

export async function addResourceRequest(name: string, taskId: number, unitId: number) {
	const res = await post('resources', {
		name: name,
		task_id: taskId,
		template_id: unitId
		// TODO update template id to resource unit id
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
