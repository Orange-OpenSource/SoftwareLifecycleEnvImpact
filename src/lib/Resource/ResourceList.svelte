<script>
    import { del, patch } from '$lib/api';
import AddResource from './AddResource.svelte';
	import DeleteResource from './DeleteResource.svelte';

    /*Bound var*/
    export let task
    export let modify

	let error = ''

	async function updateResource(resource){
		const newValue = document.getElementById('typeNumber' + resource.id).value /*TODO remove this put svelte logic in place*/
		const res = await patch('resources/' + resource.id,[
			{
				op: 'replace',
				path: '/value',
				value: newValue
			}
		])

		error = '' 
		switch (res.status) {
            case undefined:
				resource.value = res.value
				break;
			case 403:
				error = 'Patch format is incorrect'
				break;
            case 404:
                error = 'No resource found with this id' + resource.id
				break;
            default:
                error = res.status + ' error'
				break;
        }
	}
</script>

{#if task.resources != null}
	<ul class="list-group list-group-flush">
		{#each task.resources as resource}
			<li class="list-group-item">
				<div class="d-flex w-100 justify-content-between align-items-center">
					<div>
						<label class="input-group-text" for="typeNumber">{resource.name}</label>
						<input type="number" id="typeNumber{resource.id}" class="form-control" readonly={!modify} value={resource.value} min=0 on:change={() => updateResource(resource)} on:click={() => {}}/>
					</div>
					
					{#if modify}
						<DeleteResource bind:task={task} {resource}/>
					{/if}
				</div>
			</li>
			{#if modify}
				{#if error != ''}
					<p style="color: red">{error}</p>
				{/if}
				{#if resource == task.resources[task.resources.length - 1]}
					<li class="list-group-item d-flex align-items-center flex-row-reverse">
						<AddResource bind:task={task}/>
					</li>
				{/if}
			{/if}
		{/each}
	</ul>
{/if}