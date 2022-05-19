const endpoint = 'http://90.84.244.180:5001/api/v1/';

/**
 * Create project in API
 *
 * @param nameProject 	name of the project
 * @returns 			the created project object
 */
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

	if (json.status === '409') alert('Project exists already');

	return json;
}

/**
 * Create model in API
 *
 * @param nameModel name of the model
 * @param idProject project id associated to model
 * @returns 		the created model object
 */
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

	if (json.status === '409') alert('Model exists already');

	return json;
}

/**
 * Update project name in API
 *
 * @param idProject 	id of project to rename
 * @param newName 		project new name
 * @returns 			updated project object
 */
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

/**
 * Update model name in API
 *
 * @param idModel 	id of model to rename
 * @param newName 	model new name
 * @returns 		updated model object
 */
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

/**
 * Get all projects from API
 *
 * @returns list of projects objects
 */
export async function getProjects() {
	const response = await fetch(endpoint + 'projects');
	return await response.json();
}

/**
 * Get base model from specific project in API
 *
 * @param idProject project id
 * @returns 		base model id
 */
export async function getOriginalModelId(idProject: any) {
	const response = await fetch(endpoint + 'projects/' + idProject);
	let res = await response.json();

	if (res.status === '404') alert('No project found with this id');

	return res.models[0];
}

/**
 * Get all models from specific project in API
 *
 * @param idProject project id
 * @returns 		list of models objects
 */
export async function getModels(idProject: any) {
	const newresponse = await fetch(endpoint + 'projects/' + idProject);
	let res = await newresponse.json();

	if (res.status === '404') alert('No project found with this id');

	return res.models;
}

/**
 * Get informations from specific model in API
 *
 * @param idModel	model id
 * @returns 		model informations
 */
export async function getModelInformations(idModel: any) {
	const newresponse = await fetch(endpoint + 'models/' + idModel);
	let res = await newresponse.json();

	if (res.status === 404) alert('No model found with this id');

	return res;
}

/**
 * Get specific task from API
 *
 * @param idTask 	task id
 * @returns 		task object
 */
export async function getTask(idTask: any) {
	const response = await fetch(endpoint + 'tasks/' + idTask);
	let res = await response.json();

	if (res.status === 404) alert('No task found with this id');

	return res;
}

/**
 * Get all tasks from specific model in API
 *
 * @param idModel 	model id
 * @returns 		list of tasks objects
 */
export async function getTasksFromModel(idModel: any) {
	const response = await fetch(endpoint + 'models/' + idModel + '/tasks');
	let res = await response.json();

	if (res.status === 404) alert('No model found with this id');

	return res;
}

/**
 * Create task in API
 *
 * @param idModel 		model id associated to task
 * @param taskName 		task name
 * @param parentTaskId  parent task id
 * @param template_id   template id
 * @returns 			the created task object
 */
export async function createTask(idModel: any, taskName: any, parentTaskId: any, template_id: any) {
	const res = await fetch(endpoint + 'tasks', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify({
			model_id: idModel,
			name: taskName,
			parent_task_id: parentTaskId,
			template_id: +template_id
		})
	});

	const json = await res.json();

	return json;
}

/**
 * Delete project in API
 *
 * @param project_id 	project id
 * @returns 			200 if successful
 */
export async function deleteProject(project_id: any) {
	const res = await fetch(endpoint + 'projects/' + project_id, {
		method: 'DELETE'
	});

	const json = await res.json();

	if (json.status === 404) alert('No project found with this id');

	return json;
}

/**
 * Delete model in API
 *
 * @param model_id 		model id
 * @returns 			200 if successful
 */
export async function deleteModel(model_id: any) {
	const res = await fetch(endpoint + 'models/' + model_id, {
		method: 'DELETE'
	});

	const json = await res.json();

	if (json.status === 404) alert('No model project with this id');
	else if (json.status === 403) alert('Cannot delete the root model of a project');

	return json;
}

/**
 * Delete task in API
 *
 * @param task_id 	task id
 * @returns 		200 if successful
 */
export async function deleteTask(task_id: any) {
	const res = await fetch(endpoint + 'tasks/' + task_id, {
		method: 'DELETE'
	});

	const json = await res.json();

	if (json.status === 404) alert('No task with this id');
	else if (json.status === 403) alert('Cannot delete the root task of a model');

	return json;
}

/**
 * Get all templates from API
 *
 * @returns list of templates
 */
export async function getTemplates() {
	const response = await fetch(endpoint + 'tasktemplates');
	let res = await response.json();

	return res;
}

/**
 * Update task name in API
 *
 * @param idTask 	task id
 * @param newName 	new name
 * @returns 		the updated task object
 */
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

/**
 * Update task parent in API
 *
 * @param idTask 			task id
 * @param parent_task_id 	parent task id
 * @returns 				the updated task object
 */
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

/**
 * Get model impact from API
 *
 * @param idModel 	model id
 * @returns 		model impact object
 */
export async function getModelImpact(idModel: any) {
	const response = await fetch(endpoint + 'models/' + idModel + '/impact');
	let res = await response.json();

	return res;
}

/**
 * Update resource value in API
 *
 * @param idResource 	resource id
 * @param value 		resource value
 * @returns 			resource object
 */
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
