import type { PatchDocument } from '$lib/model/api/model/patchDocument';
import { patch } from './api';
import type { ResourceInput } from './model/resource';

export async function updateResourceInputRequest(resourceInput: ResourceInput): Promise<ResourceInput> {
	const patchDocument: PatchDocument[] = [
		{
			op: 'replace',
			path: '/input',
			value: resourceInput.input.toString()
		},
		{
			op: 'replace',
			path: '/days',
			value: resourceInput.days.toString()
		},
		{
			op: 'replace',
			path: '/months',
			value: resourceInput.months.toString()
		},
		{
			op: 'replace',
			path: '/years',
			value: resourceInput.years.toString()
		}
	];
	const res = await patch('resourceinputs/' + resourceInput.id, patchDocument);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
