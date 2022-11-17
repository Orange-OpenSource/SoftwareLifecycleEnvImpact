import type { Model, PatchDocument, Task } from '$lib/api/dataModel';
import { get, post, patch, del } from './api';

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
	const patchDocument: PatchDocument = {
		op: 'replace',
		path: '/name',
		value: newName
	};
	const res = await patch('models/' + model.id, [patchDocument]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function deleteModelRequest(model: Model): Promise<Model> {
	const res = await del('models/' + model.id);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function duplicateModelRequest(model: Model): Promise<Model> {
	const res = await post('models/' + model.id + '/copy', '');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
