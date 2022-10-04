import { get, post } from './api';
import type { ServerImpact } from '$lib/model/serverImpact';
import type { UsageServer } from '$lib/model/usageServer';
import type { ConfigurationServer } from '$lib/model/configurationServer';

export async function getDefaultModelsName(): Promise<string[]> {
	const res = await get('server/all_default_models');
	return res.text().then((json) => {
		return JSON.parse(json);
	});
}

export async function getServerImpactByModelName(modelName: string): Promise<ServerImpact> {
	const params = '?archetype=' + modelName + '&verbose=false';
	const res = await get('server/model' + params);
	return res.text().then((json) => {
		return JSON.parse(json);
	});
}

export async function getServerImpactByConfig(
	config: ConfigurationServer,
	usage: UsageServer
): Promise<ServerImpact> {
	console.log({
		configuration: config,
		usage: usage
	});
	const params = '?verbose=true&allocation=TOTAL';
	const res = await post('server' + params, {
		configuration: config,
		usage: usage
	});
	return res.text().then((json) => {
		console.log(json);
		return JSON.parse(json);
	});
}
