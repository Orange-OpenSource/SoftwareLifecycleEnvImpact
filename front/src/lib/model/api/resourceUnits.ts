import { get } from './api';
import type { ResourceUnit } from './model/resource';

export async function getResourceUnitsRequest(): Promise<Array<ResourceUnit>> {
	const res = await get('resourcetemplates');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
