<script>
	import { del } from '$lib/api';
	import Modal from '$lib/Modal.svelte';

    /*Bound var*/
    export let task

    export let resource
    
    let showModal = false
    let error = ''

    async function deleteResource(resource){
        const res = await del('resources/'+resource.id)

        error = '' 
		switch (res.status) {
            case undefined:
                task.resources = task.resources.filter(r => r.id != resource.id);
                showModal = false;
				break;
            case 404:
                error = 'No resource found with this id '+resource.id
				break;
            default:
                error = res.status + ' error'
				break;
        }
    }
</script>

<input on:click|stopPropagation={() => showModal = true} type="image" src="/trash.svg" width="25" height="25" alt="Bin" loading="lazy"/>

<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{resource.name}</strong> ?</span>
    
    {#if error != ''}
        <p style="color: red">{error}</p>
    {/if}

	<button on:click|stopPropagation={() => deleteResource(resource)} slot="btnsave" type="button" class="btn btn-danger">Delete</button>
</Modal>
