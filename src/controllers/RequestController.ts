const endpoint = 'http://90.84.244.180:5001/api/v1/';
const mockendpoint = 'https://626131b3327d3896e2767e8e.mockapi.io/';

export async function createProject() {
    const res = await fetch(mockendpoint + "projects", {
        method: 'POST'
    })

    const json = await res.json();
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
    const response = await fetch(mockendpoint + "projects");
    return await response.json();
}

export async function getOriginalModelId(idProject) {
    const response = await fetch(mockendpoint + "projects/" + idProject);
    let res = await response.json();

    return res.models[0];
}

export async function getModels(idProject) {
    const newresponse = await fetch(mockendpoint + "projects/" + idProject);
    let res = await newresponse.json();

    return res.models;
}

export async function getModel(idModel) {
    const newresponse = await fetch(mockendpoint + "models/" + idModel);
    let res = await newresponse.json();

    return res.content;
}