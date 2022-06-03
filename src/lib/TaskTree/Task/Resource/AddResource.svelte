<script>
    import Modal from '$lib/Modal.svelte';
	import { get, post } from '$lib/api';

    /*Bound var*/
    export let task

    let resourceTemplates = getResourceTemplate()
    let selectedTemplate;

    async function getResourceTemplate() {
        const res = await get('resourcetemplates')
		if (res.status === 404) throw new Error('Cannot retrieve resource templates');
		else {
			return res
		}
    }
    
    async function handleSubmit(){
		if(selectedTemplate != null){
			const res = await post('resources', {
                name: selectedTemplate.name,
                task_id: task.id,
                template_id: selectedTemplate.id,
			})

			if (res.status === 409) alert('Resource already exist');
			else{
				task.resources.push(res)
				/*Redondant assignment to force Svelte to update components*/
				task.resources = task.resources
			}
		}
	}
</script>

<input on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalCreateResource{task.id}" type="image" src="/add.svg" width="25" height="25" alt="Bin" loading="lazy"/>

<Modal details={'CreateResource' + task.id}>
    <span slot="title">Create new resource :</span>
    <form slot="body" on:submit|preventDefault={handleSubmit}>
        {#await resourceTemplates}
            <p>Loading resource templates</p>
        {:then resourceTemplates}
            <select class="form-select" bind:value={selectedTemplate}>
                <option value={null} disabled selected class="form-check-input"> -- Templates -- </option>
                {#each resourceTemplates as template}
                    <option value={template}>{template.name}</option>
                {/each}
            </select>
        {:catch error}
            <p style="color: red">{error.message}</p>
        {/await}
        
        <button data-bs-dismiss="modal" type="submit" class="btn btn-primary">Create resource</button>
    </form>
</Modal>