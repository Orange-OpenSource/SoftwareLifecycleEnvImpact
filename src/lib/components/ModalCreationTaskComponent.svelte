<script lang="ts">
	export let task_id: any;
</script>

<div
	class="modal fade"
	id="modalCreateTask{task_id}"
	tabindex="-1"
	aria-labelledby="modalLabelCreate{task_id}"
	aria-hidden="true"
>
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="modalLabelCreate{task_id}"><slot name="taskName" /></h5>
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
