<script lang="ts">
	import type { Model } from 'src/model/model';

	export let selectedModel: Model;

	/* Bound var */
	export let modify: boolean;
</script>

{#if selectedModel == undefined}
	<div>No model selected</div>
{:else}
	<div class="row" style="padding : 20px 0px 0px 10px; margin-bottom: 20px;">
		<span class="col">
			<div class="card">
				<h5 class="card-body">
					{selectedModel.name}
				</h5>
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
