<script lang="ts">
	import type { Model, Task } from '$lib/api/dataModel';

	export let selectedModel: Model;

	/* Bound var */
	export let modify: boolean;
</script>

{#if selectedModel == undefined}
	<div>No model selected</div>
{:else}
	<div class="row sticky-top">
		<input class="form-check-input" type="checkbox" bind:checked={modify} id="editmodeSwitch" />
		<label class="form-check-label" for="editmodeSwitch">Editing mode</label>
	</div>
{/if}
