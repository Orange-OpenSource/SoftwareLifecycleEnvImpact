const endpoint = 'http://90.84.244.180:5001/api/v1/';
const mockendpoint = 'https://626131b3327d3896e2767e8e.mockapi.io/';

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

	return json.id;
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

export async function updateModel(idModel: any) {
	/*
    const res = await fetch(endpoint+"models/"+idModel, {
        method: 'PUT'
    })

    const json = await res.json();
    */
	return idModel;
}

export async function getProjects() {
	const response = await fetch(endpoint + 'projects');
	return await response.json();
}

export async function getOriginalModelId(idProject: any) {
	const response = await fetch(endpoint + 'projects/' + idProject);
	let res = await response.json();

	return res.models[0];
}

export async function getModels(idProject: any) {
	const newresponse = await fetch(endpoint + 'projects/' + idProject);
	let res = await newresponse.json();

	return res.models;
}

export async function getModel(idModel: any) {
	const newresponse = await fetch(mockendpoint + 'models/' + idModel);
	let res = await newresponse.json();

	return res.content;
}

export async function getModelInformations(idModel: any) {
	const newresponse = await fetch(endpoint + 'models/' + idModel);
	let res = await newresponse.json();

	return res;
}

export async function getTask(idTask: any) {
	const response = await fetch(endpoint + 'tasks/' + idTask);
	let res = await response.json();

	return res;
}

export async function getTaskInput(idTaskInput: any) {
	const response = await fetch(endpoint + 'taskinputs/' + idTaskInput);
	let res = await response.json();

	return res;
}

export async function getTasksFromModel(idModel: any) {
	const response = await fetch(endpoint + 'models/' + idModel + '/tasks');
	let res = await response.json();

	return res;
}

export async function createTask(idModel: any, taskName: any, parentTaskId: any, taskTypeId: any) {
	const res = await fetch(endpoint + 'models', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify({
			model_id: idModel,
			name: taskName,
			parent_task_id: parentTaskId,
			task_type_id: taskTypeId
		})
	});

	const json = await res.json();

	return json;
}
