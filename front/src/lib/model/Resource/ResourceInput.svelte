<script lang="ts">
	import type { ResourceInput } from '$lib/model/api/model/resource';
	import { updateResourceInputRequest } from '../api/resource_input';
	import Error from '$lib/Error.svelte';

	/*Bound var*/
	export let resourceInput: ResourceInput;

	export let modify: boolean;
	let error = '';

	async function updateResource() {
		try {
			await updateResourceInputRequest(resourceInput);
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<input type="number" id="typeNumber{resourceInput.input}" class="form-control" readonly={!modify} bind:value={resourceInput.input} min="1" on:change={() => updateResource()} on:click={() => {}} />
<input type="number" id="typeNumber{resourceInput.days}" class="form-control" readonly={!modify} bind:value={resourceInput.days} min="0" on:change={() => updateResource()} on:click={() => {}} />
<input type="number" id="typeNumber{resourceInput.months}" class="form-control" readonly={!modify} bind:value={resourceInput.months} min="0" on:change={() => updateResource()} on:click={() => {}} />
<input type="number" id="typeNumber{resourceInput.years}" class="form-control" readonly={!modify} bind:value={resourceInput.years} min="0" on:change={() => updateResource()} on:click={() => {}} />

{#if error}
	<Error message={error} />
{/if}
