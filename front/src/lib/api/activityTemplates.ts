import type { ActivityTemplate } from '$lib/api/dataModel';
import { get } from './api';

export async function getActivityTemplateRequest(): Promise<Array<ActivityTemplate>> {
	const res = await get('activities/templates');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
