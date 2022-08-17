import { get, patch, post } from '$lib/api/api';
import type { Model } from 'src/model/model';
import type { Task } from 'src/model/task';

export async function getModelTasksRequest(modelId: number): Promise<Task> {
	const res = await get('models/' + modelId + '/tasks');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function createModelRequest(name: string, project_id: number): Promise<Model> {
	const res = await post('models', {
		name: name,
		project_id: project_id
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function renameModelRequest(model: Model, newName: string) {
	const res = await patch('models/' + model.id, [
		{
			op: 'replace',
			path: '/name',
			value: newName
		}
	]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
