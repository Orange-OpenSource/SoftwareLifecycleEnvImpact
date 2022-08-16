import { get } from '$lib/api/api';
import type { TaskTemplate } from 'src/model/taskTemplate';

export async function getTaskTemplates(): Promise<Array<TaskTemplate>> {
	const res = await get('tasktemplates');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
