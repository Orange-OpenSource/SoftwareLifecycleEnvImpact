const endpoint = 'http://90.84.244.180:5001/api/v1/';
const mockendpoint = 'https://626131b3327d3896e2767e8e.mockapi.io/';

export async function createProject(nameProject) {
    const res = await fetch(endpoint + "projects", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            "name" : nameProject
        })
    })


    const json = await res.json();

    /* Création d'un modèle directement après la création du projet
    const newres = await fetch(endpoint + "models", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            "name" : "First model",
            "id" : json.id
        })
    })

    const newjson = await newres.json();

    return newjson.id;
    */

    return json.models[0];
}

export async function updateModel(idModel) {
    /*
    const res = await fetch(endpoint+"models/"+idModel, {
        method: 'PUT'
    })

    const json = await res.json();
    */
    return idModel;
}

export async function getProjects() {
    const response = await fetch(endpoint + "projects");
    return await response.json();
}

export async function getOriginalModelId(idProject) {
    const response = await fetch(endpoint + "projects/" + idProject);
    let res = await response.json();

    return res.models[0];
}

export async function getModels(idProject) {
    const newresponse = await fetch(endpoint + "projects/" + idProject);
    let res = await newresponse.json();

    return res.models;
}

export async function getModel(idModel) {
    const newresponse = await fetch(mockendpoint + "models/" + idModel);
    let res = await newresponse.json();

    return res.content;
}

export async function getModelInformations(idModel) {
    const newresponse = await fetch(endpoint + "models/" + idModel);
    let res = await newresponse.json();

    return res;
}

export async function getTask(idTask) {
    const response = await fetch(endpoint + "tasks/" + idTask);
    let res = await response.json();

    return res;
}

export async function getTaskInput(idTaskInput) {
    const response = await fetch(endpoint + "taskinputs/" + idTaskInput);
    let res = await response.json();

    return res;
}

export async function getTasksFromModel(idModel) {
    const response = await fetch(endpoint + "models/" + idModel + "/tasks");
    let res = await response.json();

    return res;
}