<script>
	export let model_name;
</script>

<div class="row" style="padding-top : 20px; margin-bottom: 20px;">
	<span class="col-3">
		<input
			type="email"
			class="form-control"
			id="nameproject"
			placeholder="Name project"
			value={model_name}
		/>
	</span>
	<button type="button" class="col-3 btn btn-light" style="margin-right: 10px;">Compare</button>
	<button type="button" class="col-3 btn btn-light" style="margin-right: 10px;">Projects</button>
	<slot />
</div>
