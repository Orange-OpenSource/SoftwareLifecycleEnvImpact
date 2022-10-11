import type { PatchDocument } from '$lib/model/api/model/patchDocument';
import type { Project } from '$lib/model/api/model/project';
import { del, get, patch, post } from './api';

export async function getProjectsRequest(): Promise<Project[]> {
	const res = await get('projects');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function getProjectRequest(projectId: number): Promise<Project> {
	const res = await get('projects/' + projectId);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function exportProjectRequest(projectId: number): Promise<string> {
	const res = await get('projects/' + projectId + '/export');
	return res.text();
}

export async function createProjectRequest(name: string): Promise<Project> {
	const res = await post('projects', {
		name: name
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function importProjectRequest(project: string): Promise<Project> {
	const res = await post('projects/import', JSON.parse(project));
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function renameProjectRequest(project: Project, name: string): Promise<Project> {
	const patchDocument: PatchDocument = {
		op: 'replace',
		path: '/name',
		value: name
	};
	const res = await patch('projects/' + project.id, [patchDocument]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function deleteProjectRequest(project: Project): Promise<Project> {
	const res = await del('projects/' + project.id);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
