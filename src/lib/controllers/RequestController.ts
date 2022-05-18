const endpoint = 'http://90.84.244.180:5001/api/v1/';

export async function createProject(nameProject: any) {
	const res = await fetch(endpoint + 'projects', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify({
			name: nameProject
		})
	});

	const json = await res.json();

	return json;
}

export async function createModel(nameModel: string, idProject: any) {
	const res = await fetch(endpoint + 'models', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify({
			name: nameModel,
			project_id: +idProject
		})
	});

	const json = await res.json();

	return json;
}

export async function updateProject(idProject: any, newName: string) {
	const res = await fetch(endpoint + 'projects/' + idProject, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify([
			{
				op: 'replace',
				path: '/name',
				value: newName
			}
		])
	});

	const json = await res.json();

	if (json.status === '403') alert('Patch format is incorrect');
	else if (json.status === '404') alert('No project with this id');

	return json;
}

export async function updateModel(idModel: any, newName: string) {
	const res = await fetch(endpoint + 'models/' + idModel, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify([
			{
				op: 'replace',
				path: '/name',
				value: newName
			}
		])
	});

	const json = await res.json();

	if (json.status === 403) alert('Patch format is incorrect');
	else if (json.status === 404) alert('No model found with this id');

	return idModel;
}

export async function getProjects() {
	const response = await fetch(endpoint + 'projects');
	return await response.json();
}

export async function getOriginalModelId(idProject: any) {
	const response = await fetch(endpoint + 'projects/' + idProject);
	let res = await response.json();

	if (res.status === '404') alert('No project found with this id');

	return res.models[0];
}

export async function getModels(idProject: any) {
	const newresponse = await fetch(endpoint + 'projects/' + idProject);
	let res = await newresponse.json();

	if (res.status === '404') alert('No project found with this id');

	return res.models;
}

export async function getModelInformations(idModel: any) {
	const newresponse = await fetch(endpoint + 'models/' + idModel);
	let res = await newresponse.json();

	if (res.status === 404) alert('No model found with this id');

	return res;
}

export async function getTask(idTask: any) {
	const response = await fetch(endpoint + 'tasks/' + idTask);
	let res = await response.json();

	if (res.status === 404) alert('No task found with this id');

	return res;
}

export async function getTaskInput(idTaskInput: any) {
	const response = await fetch(endpoint + 'taskinputs/' + idTaskInput);
	let res = await response.json();

	if (res.status === 404) alert('No task input found with this id');

	return res;
}

export async function getTasksFromModel(idModel: any) {
	const response = await fetch(endpoint + 'models/' + idModel + '/tasks');
	let res = await response.json();

	if (res.status === 404) alert('No model found with this id');

	return res;
}

export async function createTask(idModel: any, taskName: any, parentTaskId: any) {
	const res = await fetch(endpoint + 'tasks', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify({
			model_id: idModel,
			name: taskName,
			parent_task_id: parentTaskId
		})
	});

	const json = await res.json();

	return json;
}

export async function deleteProject(project_id: any) {
	const res = await fetch(endpoint + 'projects/' + project_id, {
		method: 'DELETE'
	});

	const json = await res.json();

	if (json.status === 404) alert('No project found with this id');

	return json;
}

export async function deleteModel(model_id: any) {
	const res = await fetch(endpoint + 'models/' + model_id, {
		method: 'DELETE'
	});

	const json = await res.json();

	if (json.status === 404) alert('No model project with this id');
	else if (json.status === 403) alert('Cannot delete the root model of a project');

	return json;
}

export async function deleteTask(task_id: any) {
	const res = await fetch(endpoint + 'tasks/' + task_id, {
		method: 'DELETE'
	});

	const json = await res.json();

	if (json.status === 404) alert('No task with this id');
	else if (json.status === 403) alert('Cannot delete the root task of a model');

	return json;
}

export async function getTemplates() {
	const response = await fetch(endpoint + 'tasktemplates');
	let res = await response.json();

	return res;
}

export async function updateTask(idTask: any, newName: string) {
	const res = await fetch(endpoint + 'tasks/' + idTask, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify([
			{
				op: 'replace',
				path: '/name',
				value: newName
			}
		])
	});

	const json = await res.json();

	if (json.status === 403) alert('Patch format is incorrect');
	else if (json.status === 404) alert('No task found with this id');

	return json;
}

export async function updateParentTask(idTask: any, parent_task_id: string) {
	const res = await fetch(endpoint + 'tasks/' + idTask, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify([
			{
				op: 'replace',
				path: '/parent_task_id',
				value: parent_task_id.toString()
			}
		])
	});

	const json = await res.json();

	if (json.status === 403) alert('Patch format is incorrect');
	else if (json.status === 404) alert('No task found with this id');

	return json;
}

export async function getModelImpact(idModel: any) {
	const response = await fetch(endpoint + 'models/' + idModel + '/impact');
	let res = await response.json();

	return res;
}

export async function updateResource(idResource: any, value: any) {
	const res = await fetch(endpoint + 'resource/' + idResource, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify([
			{
				op: 'replace',
				path: '/value',
				value: value
			}
		])
	});

	const json = await res.json();

	if (json.status === 403) alert('Patch format is incorrect');
	else if (json.status === 404) alert('No model found with this id');

	return json;
}
