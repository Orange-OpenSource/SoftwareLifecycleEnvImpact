<script lang="ts">
	export let yearsExpectancy: number = 1;
</script>

<label for="lifeExpectancy">Years</label>
<input
    bind:value={yearsExpectancy}
    type="number"
    class="form-control"
    id="lifeExpectancy"
    min="10"
    max="10000"
    step="10"
/>
