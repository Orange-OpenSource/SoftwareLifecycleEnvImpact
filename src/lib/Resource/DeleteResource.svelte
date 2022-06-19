<script>
	import { del } from '$lib/api';
	import ModalComponent from '$lib/Modal.svelte';

    /*Bound var*/
    export let task

    export let resource

    async function deleteResource(resource){
        const res = await del('resources/'+resource.id)
        
        if (res.status === 404) alert('No resource found with this id '+resource.id);
        else{
            task.resources = task.resources.filter(r => r.id != resource.id);
        }
    }
</script>

<input on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalDeleteResource{resource.id}" type="image" src="/trash.svg" width="25" height="25" alt="Bin" loading="lazy"/>

<ModalComponent details="DeleteResource{resource.id}">
	<span slot="title">Confirm delete</span>

	<span slot="body">Are you sure you want to delete <strong>{resource.name}</strong> ?</span>

	<button on:click|stopPropagation={() => deleteResource(resource)} slot="btnsave" type="button" data-bs-dismiss="modal" class="btn btn-danger">Delete</button>
</ModalComponent>
