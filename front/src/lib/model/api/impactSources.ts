import { get } from './api';

export async function getImpactSources(): Promise<Array<string>> {
	const res = await get('impactsources');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
