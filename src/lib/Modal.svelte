<script>
	/*Bound var*/
	export let showModal;
</script>

{#if showModal}
  <div class="modal" id="sampleModal" tabindex="-1" role="dialog" aria-labelledby="sampleModalLabel" aria-hidden={false}>
		<div class="modal-dialog modal-dialog-centered" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<div class="w-100 d-flex justify-content-between">
						<h5 class="modal-title"><slot name="title" /></h5>
						<slot name="btndelete" />
					</div>
					<button type="button" class="btn-close" on:click|stopPropagation={() => showModal = false} aria-label="Close" />
				</div>
				<div class="modal-body">
					<slot name="body" />
				</div>
				<div class="modal-footer">
					<slot name="btnsave" />
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
  .modal {
    display: block;
  }
</style>