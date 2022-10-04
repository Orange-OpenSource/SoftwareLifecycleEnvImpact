<script lang="ts">
	import type { Model } from 'src/model/model';
	import type { Task } from 'src/model/task';

	export let selectedModel: Model;

	/* Bound var */
	export let modify: boolean;
	export let selectedTask: Task;
</script>

{#if selectedModel == undefined}
	<div>No model selected</div>
{:else}
	<div class="row" style="padding : 20px 0px 0px 10px; margin-bottom: 20px;">
		<span class="col">
			<div
				on:click|stopPropagation={() => (selectedTask = selectedModel.root_task)}
				class="card {selectedModel.root_task === selectedTask ? 'border-primary' : ''}"
				style="min-width: 18rem; width: fit-content;"
			>
				<div class="card-body">
					<h5>{selectedModel.name}</h5>
				</div>
			</div>
		</span>
		<div class="col-8 form-check form-switch" style="margin:5px 0px 0px 10px;">
			<div class="float-end">
				<input class="form-check-input" type="checkbox" bind:checked={modify} id="editmodeSwitch" />
				<label class="form-check-label" style="width:100px;" for="editmodeSwitch">Editing mode</label>
			</div>
		</div>
	</div>
{/if}
