<script lang="ts">
	/*Bound var*/
	export let showModal: boolean;

	function close(){
		showModal = false
	}
</script>

{#if showModal}
	<div class="modal" id="sampleModal" tabindex="-1" role="dialog" aria-labelledby="sampleModalLabel" aria-hidden={false} on:click|stopPropagation={() => console.log('stopped propagation')}>
		<div class="modal-dialog modal-dialog-centered" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<div class="w-100 d-flex justify-content-between">
						<h5 class="modal-title"><slot name="title" /></h5>
						<slot name="btndelete" />
					</div>
					<button type="button" class="btn-close" on:click|stopPropagation={close} aria-label="Close" />
				</div>
				<div class="modal-body">
					<slot name="body" />
					<slot name="error" />
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
