<script lang="ts">
	export let showModal: boolean;

	function closeModal(event) {
		event.stopPropagation();
		showModal = false;
	}

	$: if (showModal && !document.body.classList.contains('modal-open')) {
			document.body.classList.add('modal-open');
		} else if (document.body.classList.contains('modal-open')) {
			document.body.classList.remove('modal-open');
		}
</script>

{#if showModal}
	<div class="modal fade show" tabindex="-1" role="dialog" on:click|self={closeModal}>
		<div class="modal-dialog modal-dialog-centered" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<div class="w-100 d-flex justify-content-between">
						<h5 class="modal-title"><slot name="title" /></h5>
						<slot name="btndelete" />
					</div>
					<button type="button" class="btn-close" on:click|self={closeModal} />
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
	{#if showModal}
		<div class="modal-backdrop show" />
	{/if}
{/if}

<style>
	.modal {
		display: block;
	}
</style>
