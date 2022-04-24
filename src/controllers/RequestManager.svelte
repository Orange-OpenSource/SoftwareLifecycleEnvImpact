<script>
    import { useNavigate } from "svelte-navigator";

    const navigate = useNavigate();
    const endpoint = 'https://626131b3327d3896e2767e8e.mockapi.io/projects';

    export async function createProject () {
        const res = await fetch(endpoint, {
            method: 'POST'
        })

        const json = await res.json();

        navigate("modify/"+json.baseModel);
    }

    export async function getProjects () {
		const response = await fetch(endpoint);
		return await response.json();
    }

    export async function loadPreview(idProject) {
        const response = await fetch(endpoint+"/"+idProject);
		let res = await response.json();

		let newres = await getModel(res.baseModel);

		return newres;
    }

    export async function getModels(idProject) {
        const newresponse = await fetch(endpoint+"/"+idProject);
        let res = await newresponse.json();
        
        return res.models;
    }

    export async function getModel(idModel) {
        const newresponse = await fetch("https://626131b3327d3896e2767e8e.mockapi.io/models"+"/"+idModel);
        let res = await newresponse.json();
        
        return res.content;
    }
</script>