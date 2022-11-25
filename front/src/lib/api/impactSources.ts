import { get } from './api';
import type { ImpactSource } from './dataModel';

export async function getImpactSources(): Promise<ImpactSource[]> {
	const res = await get('impactsources');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}