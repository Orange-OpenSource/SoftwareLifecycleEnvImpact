import { get } from './api';

export async function getImpactSources(): Promise<[string, string] | [string, unknown][]> {
	const res = await get('impactsources');
	return res.text().then((json: string) => {
		return Object.entries(JSON.parse(json));
	});
}
