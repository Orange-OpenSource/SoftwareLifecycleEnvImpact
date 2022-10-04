import { del, get, patch, post } from '$lib/api/api';
import type { TaskImpact } from 'src/model/impacts';
import type { PatchDocument } from 'src/model/patchDocument';
import type { Task } from 'src/model/task';

export async function renameTaskRequest(task: Task, newName: string): Promise<Task> {
	const patchDocument: PatchDocument = {
		op: 'replace',
		path: '/name',
		value: newName
	};
	const res = await patch('tasks/' + task.id, patchDocument);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function getTaskImpact(task: Task): Promise<TaskImpact> {
	const res = await get('tasks/' + task.id + '/impacts');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function deleteTaskRequest(task: Task): Promise<Task> {
	const res = await del('tasks/' + task.id);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function createTaskFromTemplateRequest(name: string, parent_task_id: number, template_id: number): Promise<Task> {
	const res = await post('tasks/templates', {
		name: name,
		parent_task_id: parent_task_id,
		template_id: template_id
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function createTaskRequest(name: string, parent_task_id: number): Promise<Task> {
	const res = await post('tasks', {
		name: name,
		parent_task_id: parent_task_id
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
