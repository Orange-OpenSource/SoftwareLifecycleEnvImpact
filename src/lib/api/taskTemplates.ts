import { get } from '$lib/api/api';
import type { TaskTemplate } from 'src/model/task';

export async function getTaskTemplatesRequest(): Promise<Array<TaskTemplate>> {
	const res = await get('tasktemplates');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
