<script>
    import { del, patch } from '$lib/api';
import AddResource from './AddResource.svelte';
	import DeleteResource from './DeleteResource.svelte';

    /*Bound var*/
    export let task
    export let modify

	async function updateResource(resource){
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

{#if task.resources != null}
	<ul class="list-group list-group-flush">
		{#each task.resources as resource}
			<li class="list-group-item">
				<div class="d-flex w-100 justify-content-between align-items-center">
					<div>
						<label class="input-group-text" for="typeNumber">{resource.name}</label>
						<input type="number" id="typeNumber{resource.id}" class="form-control" readonly={!modify} value={resource.value} min=0 on:change={() => updateResource(resource)} on:click|stopPropagation={() => {}}/>
					</div>
					
					{#if modify}
						<DeleteResource bind:task={task} {resource}/>
					{/if}
				</div>
			</li>
			{#if modify}
				<li class="list-group-item d-flex align-items-center flex-row-reverse">
					<AddResource bind:task={task}/>
				</li>
			{/if}
		{/each}
	</ul>
{/if}