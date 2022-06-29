<script>
    import Modal from '$lib/Modal.svelte';
	import { get, post } from '$lib/api';

    /*Bound var*/
    export let task

    let error = undefined
	let showModal = false

    let resourceTemplates = getResourceTemplate()
    let selectedTemplate;


    async function getResourceTemplate() {
        error = undefined
        const res = await get('resourcetemplates')
		if (res.status === 404) 
            error = 'Cannot retrieve resource templates'
		else {
			return res
		}
    }
    
    async function handleSubmit(){
		if(selectedTemplate != null){
            error = undefined
			const res = await post('resources', {
                name: selectedTemplate.name,
                task_id: task.id,
                template_id: selectedTemplate.id,
			})

            if(res.status == undefined){
                task.resources.push(res)
				/*Redondant assignment to force Svelte to update components*/
				task.resources = task.resources
                showModal = false
            }  else if (res.status === 409){
                error = 'Resource already exist'
            } else {
                error = res.status + ' error'
            }
		}
	}
</script>

<input on:click={() => showModal = true} type="image" src="/add.svg" width="25" height="25" alt="Bin" loading="lazy"/>

<Modal bind:showModal>
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

        {#if error != undefined}
            <p style="color: red">{error}</p>
        {/if}
        
        <button type="submit" data-dismiss="modal" class="btn btn-primary">Create resource</button>
    </form>
</Modal>