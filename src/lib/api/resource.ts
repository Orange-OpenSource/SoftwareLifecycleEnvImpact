import { patch, post } from '$lib/api/api';
import type { Resource } from 'src/model/resource';

export async function updateResourceRequest(resource: Resource, newValue: string): Promise<Resource> {
	const res = await patch('resources/' + resource.id, [
		{
			op: 'replace',
			path: '/value',
			value: newValue
		}
	]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function addResourceRequest(name: string, taskId: number, templateId: number){
	const res = await post('resources', {
		name: name,
		task_id: taskId,
		template_id: templateId
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}