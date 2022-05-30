<script>
	export let selectedModel;

	/* Bound var */
	export let modify;

	async function changeState() {
		let state = document.getElementById('editmodeSwitch').checked;

		if (state) enableModifications();
		else await renameModel();
	}

	function enableModifications() {
		modify = true;
	}

	/**
	 * Update the name of the model.
	 */
	async function renameModel() {
		modify = false;
		let newName = document.getElementById('nameproject').value;
		/*TODO let this one or on the side, not both*/
	}
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
				<input on:click={changeState} class="form-check-input" type="checkbox" id="editmodeSwitch" checked={modify} />
				<label class="form-check-label" style="width:100px;" for="editmodeSwitch">Editing mode</label>
			</div>
		</div>
	</div>
{/if}
