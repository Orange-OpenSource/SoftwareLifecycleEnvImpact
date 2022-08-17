import { get, patch, post } from '$lib/api/api';
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
/*TODO toutes les fonctions qui finissent par request nom pas ouf */
export async function renameProjectRequest(project: Project, name: string): Promise<Project> {
	const res = await patch('projects/' + project.id, [
		{
			op: 'replace',
			path: '/name',
			value: name
		}
	]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}
