import type { ActivityImpact, PatchDocument, Activity } from '$lib/api/dataModel';
import { patch, get, del, post } from './api';

export async function renameActivityRequest(activity: Activity, newName: string): Promise<Activity> {
	const patchDocument: PatchDocument = {
		op: 'replace',
		path: '/name',
		value: newName
	};
	const res = await patch('activities/' + activity.id, [patchDocument]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function getActivityImpact(activity: Activity): Promise<ActivityImpact> {
	const res = await get('activities/' + activity.id + '/impacts');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function deleteActivityRequest(activity: Activity): Promise<Activity> {
	const res = await del('activities/' + activity.id);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function createActivityRequest(name: string, parent_activity_id: number): Promise<Activity> {
	const res = await post('activities', {
		name: name,
		parent_activity_id: parent_activity_id
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function changeActivityParent(activity: Activity, newParent: Activity): Promise<Activity> {
	const patchDocument: PatchDocument = {
		op: 'replace',
		path: '/parent_activity_id',
		value: newParent.id.toString()
	};
	const res = await patch('activities/' + activity.id, [patchDocument]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
