<script>
    import { patch } from '$lib/api';


    /*Bound var*/
    export let resources
    export let modify

	async function updateResource(resource){
        console.log("updateResource")
		const newValue = document.getElementById('typeNumber' + resource.id).value
		const res = await patch('resource/' + resource.id,[
			{
				op: 'replace',
				path: '/value',
				value: newValue
			}
		])

		if (res.status === 403) alert('Patch format is incorrect');
		else if (res.status === 404) alert('No resource found with this id' + resource.id);
		else{
			resource.value = res.value
		}

	}
</script>

{#if resources != null}
    {#each resources as resource}
        <div class="input-group mb-3">
            <label class="input-group-text" for="typeNumber">{resource.name}</label>
            <input type="number" id="typeNumber{resource.id}" class="form-control" readonly={!modify} value={resource.value} on:change={() => updateResource(resource)} />
        </div>
    {/each}
{/if}