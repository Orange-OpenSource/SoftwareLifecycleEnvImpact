import { del, get, patch, post } from '$lib/api/api';
import type { PatchDocument } from 'src/model/patchDocument';
import type { Project } from 'src/model/project';

export async function getProjectsRequest(): Promise<Project[]> {
	const res = await get('projects');
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function getProjectRequest(projectId: string): Promise<Project> {
	const res = await get('projects/' + projectId);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function createProjectRequest(name: string): Promise<Project> {
	const res = await post('projects', {
		name: name
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function renameProjectRequest(project: Project, name: string): Promise<Project> {
	const patchDocument: PatchDocument = {
		op: OpEnum.Replace,
		path: '/name',
		value: name
	};
	const res = await patch('projects/' + project.id, patchDocument);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function deleteProjectRequest(project: Project): Promise<Project>{
	const res = await del('projects/' + project.id);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}