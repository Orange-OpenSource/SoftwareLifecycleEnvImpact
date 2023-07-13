/*
 * BSD 3-Clause License
 *
 * Copyright (c) 2017, Orange
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * * Redistributions of source code must retain the above copyright notice, this
 *   list of conditions and the following disclaimer.
 *
 * * Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 *
 * * Neither the name of the copyright holder nor the names of its
 *   contributors may be used to endorse or promote products derived from
 *   this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
import type { PatchDocument, Project } from '$lib/api/dataModel';
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
