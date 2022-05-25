<script>
	export /**
* @type {any}
*/
	 let details;
</script>

<div on:click|stopPropagation={() => {}} class="modal fade" id="modal{details}" tabindex="-1" aria-labelledby="modalLabel{details}" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<div class="w-100 d-flex justify-content-between">
					<h5 class="modal-title" id="modalLabel{details}"><slot name="title" /></h5>
					<slot name="btndelete" />
				</div>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>
			<div class="modal-body">
				<slot name="body" />
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
				<slot name="btnsave" />
			</div>
		</div>
	</div>
</div>
