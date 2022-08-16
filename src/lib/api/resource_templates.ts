import { get } from '$lib/api/api';
import type { ResourceTemplate } from 'src/model/resourceTemplate';

export async function getResourceTemplates(): Promise<Array<ResourceTemplate>> {
	const res = await get('resourcetemplates');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
