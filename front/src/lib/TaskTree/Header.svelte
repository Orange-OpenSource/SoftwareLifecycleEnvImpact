<script lang="ts">
	import type { Model, Task } from "$lib/api/dataModel";


	export let selectedModel: Model;

	/* Bound var */
	export let modify: boolean;
	export let selectedTask: Task;
</script>

{#if selectedModel == undefined}
	<div>No model selected</div>
{:else}
	<div class="row">
		<span class="col-9">
			<div
				on:click|stopPropagation={() => (selectedTask = selectedModel.root_task)}
				class="card {selectedModel.root_task === selectedTask ? 'border-primary' : ''}"
				style="min-width: 15rem; width: fit-content;"
			>
				<div class="card-body">
					<h5>{selectedModel.name}</h5>
				</div>
			</div>
		</span>
		<div class="col-3 form-switch">
			<input class="form-check-input" type="checkbox" bind:checked={modify} id="editmodeSwitch" />
			<label class="form-check-label" for="editmodeSwitch">Editing mode</label>
		</div>
	</div>
{/if}
