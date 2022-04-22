<script>
    import { useNavigate } from "svelte-navigator";

    const navigate = useNavigate();
    const endpoint = 'https://626131b3327d3896e2767e8e.mockapi.io/projects';

    export async function createProject () {
        const res = await fetch(endpoint, {
            method: 'POST'
        })

        const json = await res.json();

        navigate("visualisation/"+json.id);
    }

    export async function getProjects () {
		const response = await fetch(endpoint);
		return await response.json();
    }

    export async function loadPreview(idProject) {
        const newresponse = await fetch(endpoint+"/"+idProject);
		let res = await newresponse.json();
		return res.baseModel;
    }
</script>