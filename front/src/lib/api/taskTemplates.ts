import type { TaskTemplate } from '$lib/api/model/task';
import { get } from './api';

export async function getTaskTemplatesRequest(): Promise<Array<TaskTemplate>> {
	const res = await get('tasks/templates');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
